# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 11:57:04 2018

@author: meichengshih
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import ensemble
from sklearn import cross_validation
import matplotlib.pyplot as plt

# Read data
data=pd.read_csv('transaction_clean_week.csv')

enc = preprocessing.LabelEncoder()
data['productmeasure']=enc.fit_transform(data['productmeasure'])

# use total sale as target, since total sale amount (in terms of quantity) has unit problem
data['purchaseamount']=data['saletotalamount']*data['unitprice']

target=data['purchaseamount']
train=data.drop(['saletotalamount','purchaseamount'],axis=1)

train['productmeasure']=enc.fit_transform(train['productmeasure'])

# vidualize target
plt.hist(target, range(0,40))

# not predicting median use other percentile for more conservative prediction
clf = ensemble.GradientBoostingRegressor(loss='quantile',alpha=0.5,max_depth=7, n_estimators=120, verbose=2)

gbr=clf.fit(train,target)

# The importance matrix shows, the monthly relative prices has a small impact on target prediction
importance=pd.DataFrame({'feature':list(train.columns), 'importance':list(gbr.feature_importances_)})
score_full=cross_validation.cross_val_score(clf,train,target, scoring='median_absolute_error',cv=5, verbose=2).mean()

# lets see the performance of model without relative prices
feature_keep=np.array(train.columns)[np.array(importance['importance']>0.03)]

train_reduce=train.loc[:,feature_keep]
score_reduce=cross_validation.cross_val_score(clf, train_reduce, target, scoring='median_absolute_error',cv=5, verbose=2).mean()

# the scores are almost the same, so just used the reduced matrix
train_reduce.to_csv('transaction_clean_reduced_week.csv',index=False)
target.to_csv('target_week.csv',index=False)