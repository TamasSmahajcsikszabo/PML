"""Batch-trainable versions of the nine classifiers (Jalil et al. 2023 set), so that training can stream over millions of URLs.

Common interface: `update(X, y)` is called once per batch (shard) and `epochs` times over the shards; models that cannot learn incrementally set
`sample_rows` and get that many rows at once (`fit_sample`) or merge per-batch sub-models (random forest). `predict_proba` accepts numpy arrays or DataFrames.
  log_reg, svm   SGDClassifier.partial_fit (log loss / hinge, standardised inputs)       naive_bayes   GaussianNB.partial_fit
  mlp            MLPClassifier.partial_fit, 2 epochs                                      xgboost       boosting continued shard after shard (xgb_model=previous)
  random_forest  a small forest per shard (first max_updates shards), trees merged          decision_tree, adaboost, knn   fitted on a random sample of the training rows
Each model uses THREADS cores (the runner trains several models at once)."""
import os

import numpy as np
import xgboost as xgb
from scipy.stats import loguniform
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

from common import SEED

THREADS = int(os.environ.get("BATCH_THREADS", 2))


def _two(p):
    return np.column_stack([1 - p, p])


class Batched:
    epochs, sample_rows, scaled, max_updates, scaler = 1, 0, False, None, None

    def _x(self, X):
        X = np.asarray(X, dtype=np.float32)
        return self.scaler.transform(X).astype(np.float32) if self.scaled else X

    def importance(self, n_features):
        return None


class SGDModel(Batched):
    scaled = True

    def __init__(self, loss, alpha):
        self.loss, self.m = loss, SGDClassifier(loss=loss, alpha=alpha, random_state=SEED)

    def update(self, X, y):
        self.m.partial_fit(self._x(X), y, classes=[0, 1])

    def predict_proba(self, X):
        Z = self._x(X)
        return self.m.predict_proba(Z) if self.loss == "log_loss" else _two(1 / (1 + np.exp(-self.m.decision_function(Z))))

    def importance(self, n):
        v = np.abs(self.m.coef_.ravel())
        return v / v.sum()


class NBModel(Batched):
    def __init__(self, var_smoothing):
        self.m = GaussianNB(var_smoothing=var_smoothing)

    def update(self, X, y):
        self.m.partial_fit(self._x(X), y, classes=[0, 1])

    def predict_proba(self, X):
        return self.m.predict_proba(self._x(X))


class MLPModel(Batched):
    scaled, epochs = True, 2

    def __init__(self, hidden_layer_sizes, alpha, learning_rate_init):
        self.m = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, alpha=alpha, learning_rate_init=learning_rate_init, batch_size=1024, random_state=SEED)

    def update(self, X, y):
        self.m.partial_fit(self._x(X), y, classes=[0, 1])

    def predict_proba(self, X):
        return self.m.predict_proba(self._x(X))


class ForestModel(Batched):
    max_updates = 8

    def __init__(self, trees_per_shard, max_depth, min_samples_leaf, max_features):
        self.kw, self.trees, self.rf, self.k = dict(max_depth=max_depth, min_samples_leaf=min_samples_leaf, max_features=max_features), trees_per_shard, None, 0

    def update(self, X, y):
        rf = RandomForestClassifier(n_estimators=self.trees, n_jobs=THREADS, random_state=SEED + self.k, **self.kw).fit(self._x(X), y)
        self.k += 1
        if self.rf is None:
            self.rf = rf
        else:  # bagging over shards: every tree sees one shard, the forest is their union
            self.rf.estimators_ += rf.estimators_
            self.rf.n_estimators = len(self.rf.estimators_)

    def predict_proba(self, X):
        return self.rf.predict_proba(self._x(X))

    def importance(self, n):
        return self.rf.feature_importances_


class SampleModel(Batched):
    """Non-incremental model fitted once on `sample_rows` random training rows."""

    def fit_sample(self, X, y):
        self.m.fit(self._x(X), y)

    def predict_proba(self, X):
        return self.m.predict_proba(self._x(X))


class TreeModel(SampleModel):
    sample_rows = 500_000

    def __init__(self, min_samples_leaf, ccp_alpha):
        self.m = DecisionTreeClassifier(criterion="entropy", min_samples_leaf=min_samples_leaf, ccp_alpha=ccp_alpha, random_state=SEED)

    def importance(self, n):
        return self.m.feature_importances_


class AdaModel(SampleModel):
    sample_rows = 200_000

    def __init__(self, n_estimators, max_depth, learning_rate):
        self.m = AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=max_depth), n_estimators=n_estimators, learning_rate=learning_rate, random_state=SEED)

    def importance(self, n):
        return self.m.feature_importances_


class KNNModel(SampleModel):
    scaled, sample_rows = True, 150_000

    def __init__(self, n_neighbors, weights):
        self.m = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, n_jobs=THREADS)


class XGBModel(Batched):
    def __init__(self, rounds, **params):
        self.rounds, self.booster = rounds, None
        self.params = {"objective": "binary:logistic", "tree_method": "hist", "nthread": THREADS, "seed": SEED, **params}

    def update(self, X, y):
        self.booster = xgb.train(self.params, xgb.DMatrix(self._x(X), label=y), num_boost_round=self.rounds, xgb_model=self.booster)

    def predict_proba(self, X):
        return _two(self.booster.predict(xgb.DMatrix(self._x(X))))

    def importance(self, n):
        v = np.zeros(n)
        for k, s in self.booster.get_score(importance_type="gain").items():
            v[int(k[1:])] = s
        return v / v.sum() if v.sum() else v


# name -> (factory with default settings, random-search candidates, search space); names match models.model.ZOO
BATCH_ZOO = {
    "log_reg": (lambda alpha=1e-5: SGDModel("log_loss", alpha), 8, {"alpha": loguniform(1e-7, 1e-3)}),
    "svm": (lambda alpha=1e-5: SGDModel("hinge", alpha), 8, {"alpha": loguniform(1e-7, 1e-3)}),
    "naive_bayes": (lambda var_smoothing=1e-9: NBModel(var_smoothing), 5, {"var_smoothing": [1e-12, 1e-9, 1e-6, 1e-3, 1e-1]}),
    "knn": (lambda n_neighbors=11, weights="distance": KNNModel(n_neighbors, weights), 6, {"n_neighbors": [3, 11, 25, 51], "weights": ["uniform", "distance"]}),
    "decision_tree": (lambda min_samples_leaf=5, ccp_alpha=0.0: TreeModel(min_samples_leaf, ccp_alpha), 6, {"min_samples_leaf": [2, 5, 20, 50], "ccp_alpha": [0.0, 1e-5, 1e-4]}),
    "adaboost": (lambda n_estimators=100, max_depth=2, learning_rate=1.0: AdaModel(n_estimators, max_depth, learning_rate), 6,
                 {"n_estimators": [50, 100, 200], "max_depth": [2, 3, 4], "learning_rate": [0.5, 1.0]}),
    "mlp": (lambda hidden_layer_sizes=(64,), alpha=1e-4, learning_rate_init=1e-3: MLPModel(hidden_layer_sizes, alpha, learning_rate_init), 8,
            {"hidden_layer_sizes": [(64,), (128,), (128, 64)], "alpha": loguniform(1e-5, 1e-1), "learning_rate_init": loguniform(1e-3, 1e-2)}),
    "random_forest": (lambda trees_per_shard=20, max_depth=None, min_samples_leaf=5, max_features="sqrt": ForestModel(trees_per_shard, max_depth, min_samples_leaf, max_features), 6,
                      {"max_depth": [None, 16, 24], "min_samples_leaf": [3, 5, 10], "max_features": ["sqrt", 0.2, 0.4]}),
    "xgboost": (lambda rounds=20, **kw: XGBModel(rounds, **{"max_depth": 6, "eta": 0.05, "min_child_weight": 1, "subsample": 0.8, "colsample_bytree": 0.8, **kw}), 14,
                {"rounds": [10, 20, 40], "max_depth": [4, 6, 8, 10], "eta": loguniform(0.02, 0.3), "min_child_weight": [1, 3, 5, 10], "subsample": [0.6, 0.8, 1.0],
                 "colsample_bytree": [0.4, 0.6, 0.8, 1.0], "reg_lambda": loguniform(0.1, 20)}),
}
