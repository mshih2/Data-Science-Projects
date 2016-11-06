import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization

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
                    xc,
                    yc,
                    "log_loss",
                    cv=4).mean()

## accuracy: 
#rfcBO = BayesianOptimization(rfcv, {'n_estimators': (397),
#                                         'min_samples_split': (1),
#                                         'max_features': (0.4653),
#                                         'min_samples_leaf':(1)})

## logloss: 0.50809
#rfcBO = BayesianOptimization(rfcv, {'n_estimators': (730),
#                                         'min_samples_split': (6),
#                                         'max_features': (0.3609),
#                                         'min_samples_leaf':(1)})

rfcBO = BayesianOptimization(rfcv, {'n_estimators': (100, 800),
                                         'min_samples_split': (1, 15),
                                         'max_features': (0.05, 1),
                                         'min_samples_leaf':(1,10)})

rfcBO.maximize(init_points=35, n_iter=285)
rfcBO.res["max"]

etime = float(time.time()-stime)