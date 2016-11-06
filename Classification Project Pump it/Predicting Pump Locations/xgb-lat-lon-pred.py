# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 21:23:27 2016

@author: meichengshih
"""

import pandas as pd
import time
import xgboost as xgb

stime = time.time()

train=pd.read_csv('./train-c.csv',index_col=0)
test=pd.read_csv('./test-c.csv',index_col=0)

traint=pd.read_csv('./lat-train-c.csv',index_col=0)
testt=pd.read_csv('./lat-test-c.csv',index_col=0)
targett=pd.read_csv('./lat-target.csv',index_col=0,header=None)
traing=pd.read_csv('./lon-train-c.csv',index_col=0)
testg=pd.read_csv('./lon-test-c.csv',index_col=0)
targetg=pd.read_csv('./lon-target.csv',index_col=0,header=None)

## Latitude
est=xgb.XGBRegressor(max_depth=15,
                     learning_rate=0.064959684732528264,
                     n_estimators=361,
                     gamma=0.03,
                     min_child_weight=1.4483624828673114,
                     subsample=0.90551784084608777,
                     colsample_bytree=0.91216449242846653)

est.fit(traint,targett) 
latpred=est.predict(testt) 

## Longitude
estg=xgb.XGBRegressor(max_depth=15,
                     learning_rate=0.068971344505777021,
                     n_estimators=285,
                     gamma=0.03279935577276321,
                     min_child_weight=0.52726132642619217,
                     subsample=0.94222150489256051,
                     colsample_bytree=0.96528268399227524)

estg.fit(traing,targetg) 
lonpred=estg.predict(testg)

train_ind=testt.index[testt.index<train.shape[0]]
test_ind=testt.index[testt.index>=train.shape[0]]
## exchange the lat and lon model since there was a mistake in the trainingg data
train.ix[train_ind,'latitude']=lonpred[0:len(train_ind)] 
train.ix[train_ind,'longitude']=latpred[0:len(train_ind)]
test.ix[test_ind,'latitude']=lonpred[len(train_ind):lonpred.shape[0]] 
test.ix[test_ind,'longitude']=latpred[len(train_ind):lonpred.shape[0]]            

train.to_csv('train-a.csv')
test.to_csv('test-a.csv')

etime = float(time.time()-stime)