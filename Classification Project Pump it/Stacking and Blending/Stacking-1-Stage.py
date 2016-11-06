# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:35:39 2016

@author: meichengshih
"""
import pandas as pd
import numpy as np
from xgboost.sklearn import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
import time
from sklearn.metrics import log_loss
from sklearn.cross_validation import StratifiedKFold
from sklearn.ensemble import ExtraTreesClassifier

stime = time.time()

nclass=3

trainc=pd.read_csv('./train-a.csv',index_col=0)
testc=pd.read_csv('./test-a.csv',index_col=0)
target=pd.read_csv('./target.csv',index_col=0)
nf=100

############ Start ################
outcome=target['status_group']

## Classifiers
# XGB log loss: 0.469xx              
cclf1=XGBClassifier(max_depth=14, 
              learning_rate=0.058763007858007782, n_estimators=250, 
              objective='multi:softprob', 
              nthread=8, gamma=0.68900723829945232,min_child_weight=7.655030497688963,
              subsample=0.8, colsample_bytree=0.8)
              
# XGB accuracy: 0.812238
cclf2=XGBClassifier(max_depth=15, 
              learning_rate= 0.035988911978619323, n_estimators=385, 
              objective='multi:softprob', 
              nthread=8, gamma=0.6835768993057566,min_child_weight= 4.3704412945588818,
              subsample=0.8, colsample_bytree=0.8)

#optimal RF log loss 0.481927
cclf3 = RandomForestClassifier(n_estimators=384, 
                                   min_samples_leaf=2.0017663228244533, 
                                   max_features=0.50603622676455928, 
                                   max_depth=26)

#optimal RF accuracy 0.811986
cclf4 = RandomForestClassifier(n_estimators=346, 
                                   min_samples_leaf=5.3373095433331219, 
                                   max_features=0.5112244272700085, 
                                   max_depth=25)                                  

#optimal ERT accuracy 0.81057
cclf5 = ExtraTreesClassifier(n_estimators=387,
                             min_samples_split=3.4955660368470,
                             max_features=0.66368829484855607,
                             max_depth=25)

#optimal ERT log loss:0.48293 
cclf6 = ExtraTreesClassifier(n_estimators=341,
                             min_samples_split=5.4856,
                             max_features=0.7769,
                             max_depth=25)  
                            

cclfs=[cclf1, cclf2, cclf3, cclf4, cclf5, cclf6]
## KFold
print ("Start Stacking Models")
eval_rec=np.zeros((nf,len(cclfs)))
blend_temp=np.zeros((trainc.shape[0],nclass))
blend_sub_temp=np.zeros((testc.shape[0],nclass))
blend_train=np.zeros((trainc.shape[0],nclass*len(cclfs)))
blend_sub=np.zeros((testc.shape[0],nclass*len(cclfs)))

for j, clf in enumerate(cclfs):
    print (str(j)+"th Classifier")
    ### K-Fold with Shufffle
    skf = list(StratifiedKFold(outcome, nf))
    for i in xrange(nf):
        train, test=skf[i]
        xtrain, xtest = trainc.ix[train,:], trainc.ix[test,:]
        ytrain, ytest = outcome.ix[train], outcome.ix[test]
        clf.fit(xtrain, ytrain)
        ytest_pred = clf.predict_proba(xtest)
        blend_temp[test]=ytest_pred
        sub_pred = clf.predict_proba(testc)
            
        if i==0:
            blend_sub_temp=sub_pred
        else:
            blend_sub_temp=blend_sub_temp+sub_pred
                
        print (i, log_loss(ytest,ytest_pred), (time.time()-stime))
        eval_rec[i,j]=log_loss(ytest,ytest_pred)
    blend_train[:,nclass*j:nclass*j+nclass]=blend_temp
    blend_sub[:,nclass*j:nclass*j+nclass]=blend_sub_temp/float(nf)
        
np.savetxt("blend_train7_500.txt",blend_train) 
np.savetxt("blend_pred7_500.txt",blend_sub) 
np.savetxt("outcome.txt",outcome) 




etime = float(time.time()-stime)