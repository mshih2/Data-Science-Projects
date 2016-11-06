import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization

stime = time.time()

dogname="/Users/meichengshih/Dropbox/Kaggle/Shelter Animal Outcomes/doggroup.csv"
doggroup=pd.read_csv(dogname, index_col=False)

df = pd.read_pickle("dog_data.pkl")

dy=df["OutcomeType"]
dx=df.drop(df.columns[[1]], axis=1)


## KFold

def rfcv(
          n_estimators,
          min_samples_split, 
          max_features,
          min_samples_leaf):
    return cv_s(RandomForestClassifier(      n_estimators=int(n_estimators),
                                             min_samples_split=int(min_samples_split),
                                             max_features=min(max_features, 0.999),
                                             min_samples_leaf=int(min_samples_leaf),
                                             criterion="gini"),
                    dx,
                    dy,
                    "log_loss",
                    cv=4).mean()

## accuracy: 0.61500
#rfcBO = BayesianOptimization(rfcv, {'n_estimators': (522),
#                                         'min_samples_split': (5),
#                                         'max_features': (0.2948),
#                                         'min_samples_leaf':(1)})

## log_loss: 0.91314
#rfcBO = BayesianOptimization(rfcv, {'n_estimators': (760),
#                                         'min_samples_split': (10),
#                                         'max_features': (0.4248),
#                                         'min_samples_leaf':(3)})

rfcBO = BayesianOptimization(rfcv, {'n_estimators': (100, 800),
                                         'min_samples_split': (1, 15),
                                         'max_features': (0.05, 1),
                                         'min_samples_leaf':(1,10)})

rfcBO.maximize(init_points=35, n_iter=285)
rfcBO.res["max"]

etime = float(time.time()-stime)