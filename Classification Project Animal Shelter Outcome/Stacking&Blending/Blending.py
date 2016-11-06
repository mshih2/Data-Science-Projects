# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:35:39 2016

@author: meichengshih
"""
import pandas as pd
import numpy as np
from xgboost.sklearn import XGBClassifier
import time
import operator

stime = time.time()

outputname="/Users/meichengshih/Dropbox/Kaggle/Shelter Animal Outcomes/sample_submission.csv"
dataoutput=pd.read_csv(outputname, index_col=False)

## Load Data
df = pd.read_pickle("clean_datatest.pkl")["AnimalType"]
cat_blend = np.loadtxt("cat_blend_train7.txt")
cat_btest = np.loadtxt("cat_blend_pred7.txt")
cy = np.loadtxt("cy7.txt")
dog_blend = np.loadtxt("dog_blend_train7.txt")
dog_btest = np.loadtxt("dog_blend_pred7.txt")
dy = np.loadtxt("dy7.txt")


bclf = XGBClassifier(max_depth=3, 
              learning_rate=0.0685, n_estimators=449, 
              objective='multi:softprob', 
              nthread=8, gamma=4.2599,min_child_weight=21.8363,
              subsample=0.7930, colsample_bytree=0.4679)

#  0.43251 for 7 models stacking
#                                  'colsample_bytree' :(0.4679)
#                                  'gamma': 4.2599),  
#                                  'learning_rate': (0.0685),                                
#                                  'max_depth': (3),
#                                  'min_child_weight': (21.8363),
#                                  'n_estimators': (449),
#                                  'subsample': ( 0.7930),

bclf.fit(cat_blend,cy)
cprob=bclf.predict_proba(cat_btest)

bimportances = bclf.booster().get_fscore()
bsorted_imp = sorted(bimportances.items(), key=operator.itemgetter(1))
bsorted_imp.reverse()

cclf = XGBClassifier(max_depth=1, 
              learning_rate=0.0607, n_estimators=303, 
              objective='multi:softprob', 
              nthread=8, gamma=3.4764, min_child_weight= 10.8559,
              subsample=0.5598    , colsample_bytree=0.6374)

# 7 models: 0.87344
#                                  'colsample_bytree' :(0.6374)
#                                  'gamma': (3.4764),  
#                                  'learning_rate': (0.0607),                                
#                                  'max_depth': 1),
#                                  'min_child_weight': ( 10.8559 ,
#                                  'n_estimators': (303),
#                                  'subsample': (0.5598  ,

cclf.fit(dog_blend,dy)
dprob=cclf.predict_proba(dog_btest)
dresult=cclf.predict(dog_btest)

cimportances = cclf.booster().get_fscore()
csorted_imp = sorted(cimportances.items(), key=operator.itemgetter(1))
csorted_imp.reverse()

dataoutput.ix[df==0,1:6]=cprob
dataoutput.ix[df==1,1:6]=dprob

dataoutput.to_csv("out.csv", index=False)

etime = float(time.time()-stime)