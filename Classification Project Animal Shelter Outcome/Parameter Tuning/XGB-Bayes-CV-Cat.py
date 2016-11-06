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
xc=x.ix[x["AnimalType"]==0,:]
yc=y.ix[x["AnimalType"]==0]
xc=xc.drop("AnimalType",axis=1)

### Turning Outcome input values
output_mapping={label:idx for idx,label in enumerate(np.unique(yc))}
yc=yc.map(output_mapping)

### Turning Breed abd Cross into numbers
breed_mapping={label:idx for idx,label in 
    enumerate(np.unique(pd.concat([xc["Breed"],xc["Cross"]], axis=0)))}
xc["Breed"]=xc["Breed"].map(breed_mapping)
xc["Cross"]=xc["Cross"].map(breed_mapping)

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
                    xc,
                    yc,
                    "log_loss",
                    cv=8).mean()

### Best Cat: log_loss: 0.44981
#                                  'max_depth': (22),
#                                  'learning_rate': (0.0519),
#                                  'n_estimators': (402),
#                                  'gamma': (0.8170),
#                                  'min_child_weight': (1.039),
#                                  'subsample': (0.9892),
#                                  'colsample_bytree' :(0.5972)

### Best Cat: accuracy: 0.83339
#                                  'max_depth': (20 (can be more)),
#                                  'learning_rate': (0.0619),
#                                  'n_estimators': (237),
#                                  'gamma': (0.6564),
#                                  'min_child_weight': (1.4305),
#                                  'subsample': (0.9431),
#                                  'colsample_bytree' :(0.7469)


## Cat log_loss: 0.44981                                  
xgboostBO = BayesOpt(xgbcv,
                                 {
                                  'max_depth': (20,27),
                                  'learning_rate': (0.0001, 0.07),
                                  'n_estimators': (300,600),
                                  'gamma': (0.1, 10),
                                  'min_child_weight': (1,5),
                                  'subsample': (0.9, 1),
                                  'colsample_bytree' :(0.5, 1)
                                  })

xgboostBO.maximize(init_points=35,n_iter=225)
xgboostBO.res["max"]


etime = float(time.time()-stime)