# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 21:23:27 2016

@author: meichengshih
"""

import pandas as pd
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

stime = time.time()
train=pd.read_csv('./train-c.csv',index_col=0)
target=pd.read_csv('./target.csv',index_col=0)

def xgbcv(max_depth, 
          max_features, 
          n_estimators,
          min_samples_leaf,
          n_jobs=-1):
    return cv_s(RandomForestClassifier(max_depth=int(max_depth),
                                 max_features=max_features,
                                 n_estimators=int(n_estimators),
                                 min_samples_leaf=int(min_samples_leaf)),
                    train,
                    target['status_group'],
                    "accuracy",
                    cv=4).mean() 
## can optimize std
xgboostBO = BayesOpt(xgbcv,
                                 {
                                  'max_depth': (25,35),
                                  'max_features': (0.5, 1),
                                  'n_estimators': (100,401),
                                  'min_samples_leaf': (1,21),
                                  })                                

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=20,n_iter=130, xi=0.1,  acq="poi")

# accuracy: 0.811986
# max: 26
# max_features: 0.50603622676455928
# min_samples_leaf: 2.0017663228244533
# n_estimator:346 

# logloss: 0.481927
# max: 25
# max_features: 0.5112244272700085 
# min_samples_leaf: 5.3373095433331219
# n_estimator: 384
#           

etime = float(time.time()-stime)