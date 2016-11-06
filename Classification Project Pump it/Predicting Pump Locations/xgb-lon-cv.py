# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 21:23:27 2016

@author: meichengshih
"""

import pandas as pd
import numpy as np
import time
import xgboost as xgb
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

stime = time.time()
train=pd.read_csv('./lon-train-c.csv',index_col=0)
#test=pd.read_csv('./lon-test-c.csv',index_col=0)
target=pd.read_csv('./lon-target.csv',index_col=0,header=None)

def xgbcv(max_depth, 
          learning_rate, 
          n_estimators,
          min_child_weight,
          gamma,
          subsample,
          colsample_bytree,
          silent=True,
          nthread=8):
    return cv_s(xgb.XGBRegressor(max_depth=int(max_depth),
                                 learning_rate=learning_rate,
                                 n_estimators=int(n_estimators),
                                 silent=silent,
                                 gamma=gamma,
                                 min_child_weight=min_child_weight,
                                 subsample=subsample,
                                 colsample_bytree=colsample_bytree,
                                 objective='reg:linear'),
                    train,
                    target,
                    "mean_squared_error",
                    cv=4).mean() 
## can optimize std
xgboostBO = BayesOpt(xgbcv,
                                 {
                                  'max_depth': (11,16),
                                  'learning_rate': (0.06, 0.07),
                                  'n_estimators': (200,400),
                                  'gamma': (0.03, 0.06),
                                  'min_child_weight': (0,5),
                                  'subsample': (0.8, 1),
                                  'colsample_bytree' :(0.8, 1)
                                  })

##{'max_params': {'colsample_bytree': 0.96528268399227524,
##  'gamma': 0.03279935577276321,
##  'learning_rate': 0.068971344505777021,
##  'max_depth': 15.422705269527267,
##  'min_child_weight': 0.52726132642619217,
##  'n_estimators': 285.47448219611499,
##  'subsample': 0.94222150489256051},
## 'max_val': -0.0025829618420680177}                               
                                  
print ("Start Optimization of Longitude Model")
xgboostBO.maximize(init_points=20,n_iter=80, xi=0.1,  acq="poi")              
xgboostBO.res["max"]

etime = float(time.time()-stime)