import pandas as pd
import numpy as np
import xgboost as xgb
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

stime = time.time()

df = pd.read_pickle("clean_data.pkl")

y=df["OutcomeType"]
x=df.drop(df.columns[[1]], axis=1)

### Dog and Cat data Seperate
xd=x.ix[x["AnimalType"]==1,:]
yd=y.ix[x["AnimalType"]==1]
xd=xd.drop("AnimalType",axis=1)

### Turning Outcome input values
output_mapping={label:idx for idx,label in enumerate(np.unique(yd))}
yd=yd.map(output_mapping)

### XGB CV model
def xgbcv(
           max_depth, 
          learning_rate, 
          n_estimators,
          min_child_weight,
          gamma,
          subsample,
          colsample_bytree,
          silent=True,
          nthread=8):
    return cv_s(xgb.XGBClassifier(
                                             max_depth=int(max_depth),
                                             learning_rate=learning_rate,
                                             n_estimators=int(n_estimators),
                                             silent=silent,
                                             nthread=nthread,
                                             gamma=gamma,
                                             min_child_weight=min_child_weight,
                                             subsample=subsample,
                                             colsample_bytree=colsample_bytree,
                                             objective='multi:softprob'),
                    xd,
                    yd,
                    "log_loss",
                    cv=4).mean()
## Dog log_loss: 0.88746
#xgboostBO = BayesOpt(xgbcv,
#                                 {
#                                  'max_depth': (8),
#                                  'learning_rate': (0.0229),
#                                  'n_estimators': (455),
#                                  'gamma': (0.6161),
#                                  'min_child_weight': (1.8397),
#                                  'subsample': (0.9097),
#                                  'colsample_bytree' :(0.6130)
#                                  })


## Dog log_loss: 0.88746                                 
xgboostBO = BayesOpt(xgbcv,
                                 {
                                  'max_depth': (6,12),
                                  'learning_rate': (0.01, 0.04),
                                  'n_estimators': (350,550),
                                  'gamma': (0.5, 0.8),
                                  'min_child_weight': (1,3),
                                  'subsample': (0.85, 0.95),
                                  'colsample_bytree' :(0.55, 0.75)
                                  })

xgboostBO.maximize(init_points=35,n_iter=205)
xgboostBO.res["max"]


etime = float(time.time()-stime)