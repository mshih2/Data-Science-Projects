# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 21:23:27 2016

@author: meichengshih
"""

import pandas as pd
import time
import xgboost as xgb
import operator
import numpy as np

stime = time.time()
#train=np.loadtxt("blend_train7.txt")[:,0:18]
#test=np.loadtxt("blend_pred7.txt")[:,0:18]
train=np.loadtxt("blend_train8_50.txt")
test=np.loadtxt("blend_pred8_50.txt")
target=pd.read_csv('./target.csv',index_col=0)
submission=pd.read_csv('./submission.csv')

est=xgb.XGBClassifier(max_depth=7,
                  learning_rate= 0.023577270815059184,
                  n_estimators=189,
                  gamma=0.074789906865142142,
                  min_child_weight=3.066587035368701,
                  subsample=0.49697592546415631,
                  colsample_bytree=0.95166695052920525,
                  reg_alpha=0.20645978460961734,
                  objective='multi:softmax')
                 
est.fit(train,target['status_group'])
pred=est.predict(test)
importances = est.booster().get_fscore()
sorted_imp = sorted(importances.items(), key=operator.itemgetter(1))

output=np.chararray(len(pred), itemsize=30)
output[pred==0]='functional'
output[pred==1]='functional needs repair'
output[pred==2]='non functional'

submission['status_group']=output
submission.to_csv('output.csv',index=False)
            

etime = float(time.time()-stime)