# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:35:39 2016

@author: meichengshih
"""
import pandas as pd
import numpy as np
from xgboost.sklearn import XGBClassifier
from sklearn.linear_model import LogisticRegression
import time
from sklearn.metrics import log_loss
from sklearn.cross_validation import StratifiedKFold

stime = time.time()

nclass=3

trainb=np.loadtxt("blend_train8_50.txt")
testb=np.loadtxt("blend_pred8_50.txt")
target=pd.read_csv('./target.csv',index_col=0)
nf=50

############ Start ################
outcome=target['status_group']

## Classifiers
# XGB              
cclf1=XGBClassifier(max_depth=7,
                  learning_rate= 0.023577270815059184,
                  n_estimators=189,
                  gamma=0.074789906865142142,
                  min_child_weight=3.066587035368701,
                  subsample=0.49697592546415631,
                  colsample_bytree=0.95166695052920525,
                  reg_alpha=0.20645978460961734,
                  objective='multi:softmax')
              
# logistic
cclf2=LogisticRegression(C=10**(3.0695275904605976),max_iter=800)

cclfs=[cclf1, cclf2]


## KFold
print ("Start Stacking Models")
eval_rec=np.zeros((nf,len(cclfs)))
blend_temp=np.zeros((trainb.shape[0],nclass))
blend_sub_temp=np.zeros((testb.shape[0],nclass))
blend_train=np.zeros((trainb.shape[0],nclass*len(cclfs)))
blend_sub=np.zeros((testb.shape[0],nclass*len(cclfs)))

for j, clf in enumerate(cclfs):
    print (str(j)+"th Classifier")
    ### K-Fold with Shufffle
    skf = list(StratifiedKFold(outcome, nf))
    for i in xrange(nf):
        train, test=skf[i]
        xtrain, xtest = trainb[train,:], trainb[test,:]
        ytrain, ytest = outcome[train], outcome[test]
        clf.fit(xtrain, ytrain)
        ytest_pred = clf.predict_proba(xtest)
        blend_temp[test]=ytest_pred
        sub_pred = clf.predict_proba(testb)
            
        if i==0:
            blend_sub_temp=sub_pred
        else:
            blend_sub_temp=blend_sub_temp+sub_pred
                
        print (i, log_loss(ytest,ytest_pred), (time.time()-stime))
        eval_rec[i,j]=log_loss(ytest,ytest_pred)
    blend_train[:,nclass*j:nclass*j+nclass]=blend_temp
    blend_sub[:,nclass*j:nclass*j+nclass]=blend_sub_temp/float(nf)
        
np.savetxt("blend_train_sec8_50.txt",blend_train) 
np.savetxt("blend_sub_sec8_50.txt",blend_sub) 
np.savetxt("outcome.txt",outcome) 




etime = float(time.time()-stime)