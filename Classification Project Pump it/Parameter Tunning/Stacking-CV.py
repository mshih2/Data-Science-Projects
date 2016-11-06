# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:35:39 2016

@author: meichengshih
"""
import numpy as np
from xgboost import XGBClassifier
import time
from bayes_opt import BayesianOptimization as BayesOpt
from sklearn.cross_validation import cross_val_score as cv_s

stime = time.time()

train = np.loadtxt("blend_train_sec8_50.txt")
outcome = np.loadtxt("outcome.txt")

         
def xgbcv(
          max_depth, 
          learning_rate, 
          n_estimators,
          min_child_weight,
          gamma,
          subsample,
          colsample_bytree,
          reg_alpha,
          silent=True,
          nthread=8):
    return cv_s(XGBClassifier(
                                             max_depth=int(max_depth),
                                             learning_rate=learning_rate,
                                             n_estimators=int(n_estimators),
                                             silent=silent,
                                             nthread=nthread,
                                             gamma=gamma,
                                             reg_alpha=reg_alpha,
                                             min_child_weight=min_child_weight,
                                             subsample=subsample,
                                             colsample_bytree=colsample_bytree,
                                             objective='multi:softprob'),
                    train,
                    outcome,
                    "accuracy",
                    cv=4).mean()

xgboostBO = BayesOpt(xgbcv,
                                 {
                                  'max_depth': (2,10),
                                  'learning_rate': (0.01, 0.1),
                                  'n_estimators': (100,300),
                                  'gamma': (0.01, 1),
                                  'reg_alpha':(0,1),
                                  'min_child_weight': (1,40),
                                  'subsample': (0.2, 1),
                                  'colsample_bytree' :(0.2, 1)
                                  })

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=30,n_iter=220, xi=0.02,  acq="poi")        
xgboostBO.res["max"]

## 0.82207, 50n, alldata

##{'max_params': {'colsample_bytree': 0.95166695052920525,
##  'gamma': 0.074789906865142142,
##  'learning_rate': 0.023577270815059184,
##  'max_depth': 7.4852578438401594,
##  'min_child_weight': 3.066587035368701,
##  'n_estimators': 189.43864463311203,
##  'reg_alpha': 0.20645978460961734,
##  'subsample': 0.49697592546415631},
## 'max_val': 0.82318172822230062}

## 0.82295, sec 50n, alldata

#{'max_params': {'colsample_bytree': 0.70130216097090403,
#  'gamma': 0.69463897066109681,
#  'learning_rate': 0.040302662016653092,
#  'max_depth': 2.4615169202298048,
#  'min_child_weight': 36.206644780059428,
#  'n_estimators': 187.95277504834337,
#  'reg_alpha': 0.10580023461763166,
#  'subsample': 0.23942373318396887},
# 'max_val': 0.8229460583934548}

etime = float(time.time()-stime)