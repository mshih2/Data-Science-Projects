# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 21:23:27 2016

@author: meichengshih
"""

import pandas as pd
import time
import xgboost as xgb
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

stime = time.time()
train=pd.read_csv('./train-c.csv',index_col=0)
target=pd.read_csv('./target.csv',index_col=0)

def xgbcv(max_depth,  
          learning_rate, 
          n_estimators,
          min_child_weight,
          gamma,
          subsample,
          colsample_bytree,
          reg_alpha, 
          reg_lambda,
          silent=True):
    return cv_s(xgb.XGBClassifier(max_depth=int(max_depth),
                                 learning_rate=learning_rate,
                                 n_estimators=int(n_estimators),
                                 gamma=gamma,
                                 reg_alpha=reg_alpha,
                                 min_child_weight=min_child_weight,
                                 objective='multi:softmax'),
                    train,
                    target['status_group'],
                    "accuracy",
                    cv=4).mean() 
## can optimize std
xgboostBO = BayesOpt(xgbcv,
                                 {
                                  'max_depth': (4,22),
                                  'learning_rate': (0.01, 0.2),
                                  'n_estimators': (200,600),
                                  'gamma': (0.01, 10),
                                  'min_child_weight': (1,40),
                                  'subsample': (0.2, 1),
                                  'colsample_bytree' :(0.2, 1),
                                  'reg_alpha':(0, 10),
                                  'reg_lambda':(0, 10)
                                  })                                

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=10,n_iter=110, xi=0.0,  acq="poi")

# accuracy
# max: 15
# learning:  0.035988911978619323
# n: 385
# gamma: 0.6835768993057566
# child: 4.3704412945588818
# subsample: 0.8
# colsample: 0.8
# 0.812238  

# logloss 
# max: 14
# learning: 0.058763007858007782
# n: 250
# gamma: 0.68900723829945232
# child: 7.6550304976889638
# subsample: 0.8
# colsample: 0.8
#                  

etime = float(time.time()-stime)