# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 21:23:27 2016

@author: meichengshih
"""
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

stime = time.time()
train=pd.read_csv('./train-c.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))
target=target.ix[:,1]

def xgbcv(max_depth,  
          max_features, 
          n_estimators,
          min_samples_leaf,
          n_jobs=-1):
    return cv_s(ExtraTreesRegressor(max_depth=int(max_depth),
                                 max_features=max_features,
                                 n_estimators=int(n_estimators),
                                 min_samples_leaf=int(min_samples_leaf)),
                    train,
                    target,
                    "mean_squared_error",
                    cv=4).mean() 
## can optimize std
xgboostBO = BayesOpt(xgbcv,
                                 {'max_depth': (10,30),
                                  'max_features': (0.2, 1),
                                  'n_estimators': (200,501),
                                  'min_samples_leaf': (1,21),
                                  })                                

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=50,n_iter=250, xi=0.05,  acq="poi")
xgboostBO.res["max"]

#{'max_params': {'max_depth': 25,
#  'max_features': 0.93856560366003716,
#  'min_samples_leaf': 1.204402405756321,
#  'n_estimators': 337.74955938860347},
# 'max_val': -0.019068833348385262}
           

etime = float(time.time()-stime)