# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 11:01:52 2016

@author: meichengshih
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

target=pd.read_csv('./target.csv',index_col=0)
train=pd.read_hdf('train_b.h5')

LogisticRegression(C=1.0,max_iter=800)

def lrcv(C):
    return cv_s(LogisticRegression(C=10**C),
                    train,
                    target['status_group'],
                    "log_loss",
                    cv=4).mean() 
## can optimize std
xgboostBO = BayesOpt(lrcv,
                                 {
                                  'C': (-5,2)
                                  })                                

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=20,n_iter=130, xi=0.1,  acq="poi")

## accuracy: 0.779xx
## max_inter:398
## C:0.66673083656199683

## log loss: 0.55096
## max_inter:219
## C:0.98739744823920894