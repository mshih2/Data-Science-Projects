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

cdf = pd.read_pickle("cat_data.pkl")
cdftest = pd.read_pickle("cat_datatest.pkl")
ddf = pd.read_pickle("dog_data.pkl")
ddftest = pd.read_pickle("dog_datatest.pkl")
nf=25

############ need to change back to cat parameters #############

## x, y:
cy=cdf["OutcomeType"]
cx=cdf.drop("OutcomeType",axis=1)

cx=np.array(cx)
cy=np.array(cy)
cdftest=np.array(cdftest)

### K-Fold with Shufffle
skf = list(StratifiedKFold(cy, nf))

## Classifiers
# XGB optimallog loss: 0.44981              
cclf1=XGBClassifier(max_depth=22, 
              learning_rate=0.0519, n_estimators=402, 
              objective='multi:softprob', 
              nthread=8, gamma=0.8170,min_child_weight=1.039,
              subsample=0.9892, colsample_bytree=0.5972)
              
# XGB all log_loss: 0.72068
cclf2=XGBClassifier(max_depth=11, 
              learning_rate=0.0346, n_estimators=285, 
              objective='multi:softprob', 
              nthread=8, gamma=0.7249,min_child_weight=1,
              subsample=0.8012, colsample_bytree=0.8087)

#optimal RF accuracy 0.82630
cclf3 = RandomForestClassifier(n_estimators=397, 
                                   min_samples_leaf=1, 
                                   min_samples_split=1,
                                   max_features=0.4653, 
                                   max_depth=None, 
                                   criterion="gini")

#optimal ERT accuracy 0.81220
cclf4 = ExtraTreesClassifier(n_estimators=748,
                             min_samples_split=4,
                             max_features=0.6237,
                             min_samples_leaf=1,
                             criterion="gini")

# XGB All accuracy: 0.70927
cclf5=XGBClassifier(max_depth=27, 
              learning_rate=0.0463, n_estimators=277, 
              objective='multi:softprob', 
              nthread=8, gamma=0.4552,min_child_weight=1.3451,
              subsample=0.8215, colsample_bytree=0.8179)

#optimal RF All accuracy 0.70122
cclf6 = RandomForestClassifier(n_estimators=449, 
                                   min_samples_leaf=1, 
                                   min_samples_split=2,
                                   max_features=0.3873, 
                                   max_depth=None, 
                                   criterion="gini") 

#optimal ERT All accuracy 0.71046
cclf7 = ExtraTreesClassifier(n_estimators=118,
                             min_samples_split=14,
                             max_features=0.2676,
                             min_samples_leaf=9,
                             criterion="gini")                                   

cclfs=[cclf1, cclf2, cclf3, cclf4, cclf5, cclf6, cclf7]



## KFold
print ("Cat Turn")
eval_rec=np.zeros((nf,len(cclfs)))
blend_temp=np.zeros((cx.shape[0],5))
blend_sub_temp=np.zeros((cdftest.shape[0],5))
blend_train=np.zeros((cx.shape[0],5*len(cclfs)))
blend_sub=np.zeros((cdftest.shape[0],5*len(cclfs)))

for j, clf in enumerate(cclfs):
        print (str(j)+"th Classifier")
        for i in xrange(nf):
            train, test=skf[i]
            cxtrain, xtest = cx[train], cx[test]
            cytrain, ytest = cy[train], cy[test]
            clf.fit(cxtrain, cytrain)
            ytest_pred = clf.predict_proba(xtest)
            blend_temp[test]=ytest_pred
            sub_pred = clf.predict_proba(cdftest)
            
            if i==0:
                blend_sub_temp=sub_pred
            else:
                blend_sub_temp=blend_sub_temp+sub_pred
                
            print (i, log_loss(ytest,ytest_pred))
            eval_rec[i,j]=log_loss(ytest,ytest_pred)
        blend_train[:,5*j:5*j+5]=blend_temp
        blend_sub[:,5*j:5*j+5]=blend_sub_temp/float(nf)
        
np.savetxt("cat_blend_train7.txt",blend_train) 
np.savetxt("cat_blend_pred7.txt",blend_sub) 
np.savetxt("cy7.txt",cy) 


## dx, dy:
dy=ddf["OutcomeType"]
dx=ddf.drop("OutcomeType",axis=1)

dx=np.array(dx)
dy=np.array(dy)
ddftest=np.array(ddftest)

### K-Fold with Shufffle
skf = list(StratifiedKFold(dy, nf))

## Classifiers
# XGB optimal dog log loss: 0.883xx              
dclf1=XGBClassifier(max_depth=9, 
              learning_rate=0.0185, n_estimators=553, 
              objective='multi:softprob', 
              nthread=8, gamma=0.7152,min_child_weight=1.416,
              subsample=0.8861, colsample_bytree=0.6017)

# XGB all log_loss: 0.72068
dclf2=XGBClassifier(max_depth=11, 
              learning_rate=0.0346, n_estimators=285, 
              objective='multi:softprob', 
              nthread=8, gamma=0.7249,min_child_weight=1,
              subsample=0.8012, colsample_bytree=0.8087)

#optimal RF accuracy 0.61500, 
dclf3 = RandomForestClassifier(n_estimators=522, 
                                   min_samples_leaf=1, 
                                   min_samples_split=5,
                                   max_features=0.2948, 
                                   max_depth=None, 
                                   criterion="gini")

#optimal RF accuracy 0.60750, 
dclf4 = ExtraTreesClassifier(n_estimators=520,
                             min_samples_split=12,
                             max_features=0.4047,
                             min_samples_leaf=1,
                             criterion="gini") 
# XGB accuracy: 0.70927
dclf5=XGBClassifier(max_depth=27, 
              learning_rate=0.0463, n_estimators=277, 
              objective='multi:softprob', 
              nthread=8, gamma=0.4552,min_child_weight=1.3451,
              subsample=0.8215, colsample_bytree=0.8179)

#optimal RF accuracy 0.70122
dclf6 = RandomForestClassifier(n_estimators=449, 
                                   min_samples_leaf=1, 
                                   min_samples_split=2,
                                   max_features=0.3873, 
                                   max_depth=None, 
                                   criterion="gini")                                                             

#optimal ERT All accuracy 0.71046
dclf7 = ExtraTreesClassifier(n_estimators=118,
                             min_samples_split=14,
                             max_features=0.2676,
                             min_samples_leaf=9,
                             criterion="gini")  

dclfs=[dclf1, dclf2, dclf3, dclf4, dclf5, dclf6, dclf7]



## KFold
print ("Dog Turn")
eval_rec=np.zeros((nf,len(dclfs)))
blend_temp=np.zeros((dx.shape[0],5))
blend_sub_temp=np.zeros((ddftest.shape[0],5))
blend_train=np.zeros((dx.shape[0],5*len(dclfs)))
blend_sub=np.zeros((ddftest.shape[0],5*len(dclfs)))
for j, clf in enumerate(dclfs):
        print (str(j)+"th Classifier")
        for i in xrange(nf):
            train, test=skf[i]
            dxtrain, dxtest = dx[train], dx[test]
            dytrain, dytest = dy[train], dy[test]
            clf.fit(dxtrain, dytrain)
            ytest_pred = clf.predict_proba(dxtest)
            blend_temp[test]=ytest_pred            
            sub_pred = clf.predict_proba(ddftest) 
            
            if i==0:
                blend_sub_temp=sub_pred
            else:
                blend_sub_temp=blend_sub_temp+sub_pred
                
            print (i, log_loss(dytest,ytest_pred))
            eval_rec[i,j]=log_loss(dytest,ytest_pred)
            
        blend_train[:,5*j:5*j+5]=blend_temp
        blend_sub[:,5*j:5*j+5]=blend_sub_temp/float(nf)
        
np.savetxt("dog_blend_train7.txt",blend_train) 
np.savetxt("dog_blend_pred7.txt",blend_sub) 
np.savetxt("dy7.txt",dy)

etime = float(time.time()-stime)