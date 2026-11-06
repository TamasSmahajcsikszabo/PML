"""Negative-result experiment: can a second model fix the first stage's errors?  PYTHONPATH=src .venv/bin/python src/tools/second_stage_experiment.py

Stage 1 = the run's top-3 blend (out-of-fold scores, host-grouped 5-fold CV). Stage 2 variants: boosting continuation on the stage-1 margin (xgboost base_margin),
stacking on the nine model scores (LR / XGBoost / + features), a specialist model on the uncertain score region, and an error detector.
Result (run 20261104T1417): none beats stage 1 (AUC 0.9710); see CLAUDE.md. test.csv / external_test.csv are not used."""
import warnings;warnings.filterwarnings('ignore')
import numpy as np,pandas as pd,xgboost as xgb
from sklearn.metrics import roc_auc_score,average_precision_score,roc_curve
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.linear_model import LogisticRegression
from common import clean_train,host_group,load,run_dir
from models.model import inputs
tr,_=clean_train(load('train'));y=tr.label.values;g=tr.url.map(host_group).values
oof=pd.read_csv(run_dir()/'oof_predictions.csv');assert (oof.y.values==y).all()
Z=inputs(tr.url.values);nine=['log_reg','svm','naive_bayes','knn','decision_tree','adaboost','mlp','random_forest','xgboost']
logit=lambda p:np.log(np.clip(p,1e-4,1-1e-4)/(1-np.clip(p,1e-4,1-1e-4)))
base=oof.blend_top3.values  # uncalibrated mean of top-3
folds=list(StratifiedGroupKFold(5,shuffle=True,random_state=0).split(Z,y,g))
def r1(y,p):
    f,t,_=roc_curve(y,p);return float(np.interp(.01,f,t))
def rep(n,p): print('%-34s AUC %.4f  AP %.4f  recall@1%%FPR %.3f'%(n,roc_auc_score(y,p),average_precision_score(y,p),r1(y,p)),flush=True)
rep('stage 1: blend top-3',base)
P=dict(XP=dict(n_estimators=150,max_depth=3,learning_rate=0.05,subsample=.8,colsample_bytree=.6,n_jobs=-1,random_state=0))
# S1 boosting continuation on stage-1 margin (xgboost base_margin)
for ne,lr in ((50,.05),(150,.05),(300,.05)):
    o=np.zeros(len(y))
    for a,b in folds:
        m=xgb.XGBClassifier(n_estimators=ne,max_depth=3,learning_rate=lr,subsample=.8,colsample_bytree=.6,n_jobs=-1,random_state=0)
        m.fit(Z.iloc[a],y[a],base_margin=logit(base[a]))
        o[b]=1/(1+np.exp(-(m.predict(Z.iloc[b],output_margin=True,base_margin=logit(base[b])))))
    rep(f'S1 boost-on-margin n={ne}',o)
# S2 stacking on nine OOF scores (+ features)
M=np.column_stack([logit(oof[c].values) for c in nine])
for name,X in (('S2a LR on 9 scores',M),('S2b XGB on 9 scores',M),('S2c XGB on 9 scores + features',np.column_stack([M,Z.values]))):
    o=np.zeros(len(y))
    for a,b in folds:
        m=LogisticRegression(C=1,max_iter=2000) if name.startswith('S2a') else xgb.XGBClassifier(n_estimators=150,max_depth=3,learning_rate=.05,subsample=.8,colsample_bytree=.6,n_jobs=-1,random_state=0)
        o[b]=m.fit(X[a],y[a]).predict_proba(X[b])[:,1]
    rep(name,o)
# S3 specialist on uncertain region
for lo,hi in ((.1,.99),(.2,.97),(.05,.995)):
    o=base.copy();unc=(base>lo)&(base<hi);print('  uncertain share',round(unc.mean(),3),'errors inside',round(((base>=.5)!=y)[unc].sum()/max(((base>=.5)!=y).sum(),1),3))
    for a,b in folds:
        ai=a[unc[a]];bi=b[unc[b]]
        m=xgb.XGBClassifier(n_estimators=200,max_depth=4,learning_rate=.05,subsample=.8,colsample_bytree=.6,n_jobs=-1,random_state=0).fit(np.column_stack([Z.values[ai],logit(base[ai])]),y[ai])
        o[bi]=.5*base[bi]+.5*m.predict_proba(np.column_stack([Z.values[bi],logit(base[bi])]))[:,1]
    rep(f'S3 specialist region ({lo},{hi})',o)
# S4 error detector: predict "stage-1 wrong", then flip toward 0.5 shrink
wrong=((base>=np.quantile(base[y==0],.99))!=y).astype(int);print('  stage-1 errors at 1%FPR threshold:',wrong.sum())
o=np.zeros(len(y))
for a,b in folds:
    m=xgb.XGBClassifier(n_estimators=200,max_depth=3,learning_rate=.05,subsample=.8,colsample_bytree=.6,n_jobs=-1,random_state=0).fit(np.column_stack([Z.values[a],logit(base[a]),y[a]*0]),wrong[a])
    o[b]=m.predict_proba(np.column_stack([Z.values[b],logit(base[b]),y[b]*0]))[:,1]
print('  error-detector AUC for predicting mistakes (CV): %.4f'%roc_auc_score(wrong,o))
