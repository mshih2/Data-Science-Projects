# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:35:39 2016

@author: meichengshih
"""
import numpy as np
from xgboost.sklearn import XGBClassifier
import time
from bayes_opt import BayesianOptimization as BayesOpt
from sklearn.cross_validation import cross_val_score as cv_s

stime = time.time()

dct = np.loadtxt("dog_blend_train7_2.txt")
dy = np.loadtxt("dy7_2.txt")

         
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
    return cv_s(XGBClassifier(
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
                    dct,
                    dy,
                    "log_loss",
                    cv=8).mean()

xgboostBO = BayesOpt(xgbcv,
                                 {
                                  'max_depth': (1,8),
                                  'learning_rate': (0.005, 0.1),
                                  'n_estimators': (100,600),
                                  'gamma': (0.5, 5),
                                  'min_child_weight': (1,30),
                                  'subsample': (0.2, 1),
                                  'colsample_bytree' :(0.2, 1)
                                  })

xgboostBO.maximize(init_points=35,n_iter=365)
xgboostBO.res["max"]
        


etime = float(time.time()-stime)