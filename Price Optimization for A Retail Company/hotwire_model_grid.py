# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 11:57:04 2018

@author: meichengshih
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import ensemble
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

# Read data
train=pd.read_csv('transaction_clean_reduced_week.csv')
target=pd.read_csv('target_week.csv', header=None)

# not predicting median use other percentile for more conservative prediction
clf = ensemble.GradientBoostingRegressor(loss='quantile',alpha=0.5,n_estimators=100, verbose=2)

param_grid={'max_depth':[5,7,9], 'n_estimators':[100,120,140]}

grid = GridSearchCV(clf, cv=5, n_jobs=1, param_grid=param_grid, scoring= 'mean_absolute_error')

scores=grid.fit(train,target)

best_score=scores.best_score_

model=scores.best_estimator_
