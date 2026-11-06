"""The nine classifiers of Jalil et al. (2023) as used in url_grammar (scikit-learn analogues of the paper's WEKA defaults),
with their hyper-parameter search spaces. Every model takes the numeric feature frame produced by `inputs`."""
import numpy as np
from scipy.stats import loguniform
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

import urlfeat
from common import SEED


def inputs(urls):
    """Feature frame (rows the grammar rejects become all zeros)."""
    return urlfeat.featurize(list(urls)).fillna(0)


class LinearSVCProba(LinearSVC):
    """LinearSVC whose predict_proba is the logistic of the margin (monotone: AUC and the margin-0 decision are the SVM's)."""

    def predict_proba(self, X):
        p = 1 / (1 + np.exp(-self.decision_function(X)))
        return np.column_stack([1 - p, p])


scaled = lambda m: make_pipeline(StandardScaler(), m)

# name -> (factory(**params), n random-search candidates, search space).  Spaces follow url_grammar/src/model/07_tuning/grid_search.py.
ZOO = {
    "log_reg": (lambda C=1.0: scaled(LogisticRegression(C=C, max_iter=5000)), 7, {"C": [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100]}),
    "svm": (lambda C=1.0: scaled(LinearSVCProba(C=C, loss="hinge", dual=True, max_iter=20000, random_state=SEED)), 6, {"C": [0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10]}),
    "naive_bayes": (lambda var_smoothing=1e-9: GaussianNB(var_smoothing=var_smoothing), 5, {"var_smoothing": [1e-12, 1e-9, 1e-6, 1e-3, 1e-1]}),
    "knn": (lambda n_neighbors=1, weights="uniform": scaled(KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, n_jobs=-1)), 8,
            {"n_neighbors": [1, 3, 5, 11, 25, 51], "weights": ["uniform", "distance"]}),
    "decision_tree": (lambda min_samples_leaf=1, ccp_alpha=0.0: DecisionTreeClassifier(criterion="entropy", min_samples_leaf=min_samples_leaf, ccp_alpha=ccp_alpha, random_state=SEED), 8,
                      {"min_samples_leaf": [1, 2, 5, 10, 20, 50], "ccp_alpha": [0.0, 1e-4, 1e-3]}),
    "adaboost": (lambda n_estimators=10, max_depth=1, learning_rate=1.0: AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=max_depth), n_estimators=n_estimators, learning_rate=learning_rate, random_state=SEED), 8,
        {"n_estimators": [10, 50, 100, 200], "max_depth": [1, 2, 3], "learning_rate": [0.5, 1.0]}),
    "mlp": (lambda hidden_layer_sizes=(64,), alpha=1e-4, learning_rate_init=1e-3: scaled(MLPClassifier(
        hidden_layer_sizes=hidden_layer_sizes, alpha=alpha, learning_rate_init=learning_rate_init, early_stopping=True, max_iter=300, random_state=SEED)), 8,
        {"hidden_layer_sizes": [(64,), (128,), (128, 64)], "alpha": loguniform(1e-5, 1e-1), "learning_rate_init": loguniform(1e-3, 1e-2)}),
    "random_forest": (lambda n_estimators=300, max_depth=None, min_samples_leaf=1, max_features="sqrt": RandomForestClassifier(
        n_estimators=n_estimators, max_depth=max_depth, min_samples_leaf=min_samples_leaf, max_features=max_features, n_jobs=-1, random_state=SEED), 8,
        {"max_depth": [None, 12, 24], "min_samples_leaf": [1, 2, 5], "max_features": ["sqrt", 0.2, 0.4]}),
    "xgboost": (lambda **kw: XGBClassifier(**{**dict(n_estimators=300, max_depth=6, learning_rate=0.05, min_child_weight=1, subsample=0.8, colsample_bytree=0.8,
                                                      n_jobs=-1, random_state=SEED), **kw}), 20,
                {"n_estimators": [100, 200, 400, 600], "max_depth": [3, 4, 6, 8, 10], "learning_rate": loguniform(0.02, 0.3), "min_child_weight": [1, 3, 5, 10],
                 "subsample": [0.6, 0.8, 1.0], "colsample_bytree": [0.4, 0.6, 0.8, 1.0], "reg_lambda": loguniform(0.1, 20)}),
}
