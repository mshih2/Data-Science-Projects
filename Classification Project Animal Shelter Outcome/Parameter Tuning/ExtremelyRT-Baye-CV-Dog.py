# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:09:50 2016

@author: meichengshih
"""

import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization

stime = time.time()

df = pd.read_pickle("dog_data.pkl")

dy=df["OutcomeType"]
dx=df.drop(["OutcomeType"], axis=1)

## CV process

def rfcv(
          n_estimators,
          min_samples_split, 
          max_features,
          min_samples_leaf):
    return cv_s(ExtraTreesClassifier(n_estimators=int(n_estimators),
                                             min_samples_split=int(min_samples_split),
                                             max_features=min(max_features, 0.999),
                                             min_samples_leaf=int(min_samples_leaf),
                                             criterion="gini"),
                    dx,
                    dy,
                    "accuracy",
                    cv=4).mean()

ERTBO = BayesianOptimization(rfcv, {'n_estimators': (100, 800),
                                         'min_samples_split': (1, 15),
                                         'max_features': (0.05, 1),
                                         'min_samples_leaf':(1,10)})

# 0.60705
#                             {'n_estimators': (520),
#                                         'min_samples_split': (12),
#                                         'max_features': (0.4047),
#                                         'min_samples_leaf':(1)})                                         

ERTBO.maximize(init_points=35, n_iter=365)

etime = float(time.time()-stime)