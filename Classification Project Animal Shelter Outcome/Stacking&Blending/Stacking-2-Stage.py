# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:35:39 2016

@author: meichengshih
"""
import numpy as np
from xgboost.sklearn import XGBClassifier
import time
from sklearn.metrics import log_loss
from sklearn.cross_validation import StratifiedKFold

stime = time.time()

cx = np.loadtxt("cat_blend_train7.txt")
cy = np.loadtxt("cy7.txt")
cat_test = np.loadtxt("cat_blend_pred7.txt")
dx = np.loadtxt("dog_blend_train7.txt")
dy = np.loadtxt("dy7.txt")
dog_test = np.loadtxt("dog_blend_pred7.txt")
nf=25

############ need to change back to cat parameters #############

### K-Fold with Shufffle
skf = list(StratifiedKFold(cy, nf))

## Classifiers
# XGB optimallog loss: 0.44981              
cclf1=XGBClassifier(max_depth=3, 
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

# XGB all log_loss: 0.72068
cclf2=XGBClassifier(max_depth=5, 
              learning_rate=0.0210, n_estimators=415, 
              objective='multi:softprob', 
              nthread=8, gamma=1.8719,min_child_weight=11.2435,
              subsample=0.6160, colsample_bytree=0.6919)

#                                  'colsample_bytree' :(0.6919)
#                                  'gamma': 1.8719),  
#                                  'learning_rate': (0.0210),                                
#                                  'max_depth': (5),
#                                  'min_child_weight': (11.2435),
#                                  'n_estimators': (415),
#                                  'subsample': (0.6160),

                                 

cclfs=[cclf1, cclf2]



## KFold
print ("Cat Turn")
eval_rec=np.zeros((nf,len(cclfs)))
blend_temp=np.zeros((cx.shape[0],5))
blend_sub_temp=np.zeros((cat_test.shape[0],5))
blend_train=np.zeros((cx.shape[0],5*len(cclfs)))
blend_sub=np.zeros((cat_test.shape[0],5*len(cclfs)))

for j, clf in enumerate(cclfs):
        print (str(j)+"th Classifier")
        for i in xrange(nf):
            train, test=skf[i]
            cxtrain, xtest = cx[train], cx[test]
            cytrain, ytest = cy[train], cy[test]
            clf.fit(cxtrain, cytrain)
            ytest_pred = clf.predict_proba(xtest)
            blend_temp[test]=ytest_pred
            sub_pred = clf.predict_proba(cat_test)
            
            if i==0:
                blend_sub_temp=sub_pred
            else:
                blend_sub_temp=blend_sub_temp+sub_pred
                
            print (i, log_loss(ytest,ytest_pred))
            eval_rec[i,j]=log_loss(ytest,ytest_pred)
        blend_train[:,5*j:5*j+5]=blend_temp
        blend_sub[:,5*j:5*j+5]=blend_sub_temp/float(nf)
        
np.savetxt("cat_blend_train7_2.txt",blend_train) 
np.savetxt("cat_blend_pred7_2.txt",blend_sub) 
np.savetxt("cy7_2.txt",cy) 



### K-Fold with Shufffle
skf = list(StratifiedKFold(dy, nf))

## Classifiers
# XGB optimal dog log loss: 0.883xx              
dclf1=XGBClassifier(max_depth=1, 
              learning_rate=0.0607, n_estimators=303, 
              objective='multi:softprob', 
              nthread=8, gamma=3.4764,min_child_weight=10.8559,
              subsample=0.5598, colsample_bytree=0.6374)
# 7 models: 0.87344
#                                  'colsample_bytree' :(0.6374)
#                                  'gamma': (3.4764),  
#                                  'learning_rate': (0.0607),                                
#                                  'max_depth': 1),
#                                  'min_child_weight': ( 10.8559 ,
#                                  'n_estimators': (303),
#                                  'subsample': (0.5598  ,
              
# XGB all log_loss: 0.72068
dclf2=XGBClassifier(max_depth=5, 
              learning_rate=0.0050, n_estimators=132, 
              objective='multi:softprob', 
              nthread=8, gamma=3.5794 ,min_child_weight=15.0656,
              subsample=0.4569, colsample_bytree=0.8381)
              
#  accuracy for 7 models stacking 0.62924
#                                  'colsample_bytree' :(0.8381)
#                                  'gamma': 3.5794 ),  
#                                  'learning_rate': (0.0050),                                
#                                  'max_depth': (5),
#                                  'min_child_weight': (15.0656),
#                                  'n_estimators': (132),
#                                  'subsample': (0.4569),


 

dclfs=[dclf1, dclf2]



## KFold
print ("Dog Turn")
eval_rec=np.zeros((nf,len(dclfs)))
blend_temp=np.zeros((dx.shape[0],5))
blend_sub_temp=np.zeros((dog_test.shape[0],5))
blend_train=np.zeros((dx.shape[0],5*len(dclfs)))
blend_sub=np.zeros((dog_test.shape[0],5*len(dclfs)))
for j, clf in enumerate(dclfs):
        print (str(j)+"th Classifier")
        for i in xrange(nf):
            train, test=skf[i]
            dxtrain, dxtest = dx[train], dx[test]
            dytrain, dytest = dy[train], dy[test]
            clf.fit(dxtrain, dytrain)
            ytest_pred = clf.predict_proba(dxtest)
            blend_temp[test]=ytest_pred            
            sub_pred = clf.predict_proba(dog_test) 
            
            if i==0:
                blend_sub_temp=sub_pred
            else:
                blend_sub_temp=blend_sub_temp+sub_pred
                
            print (i, log_loss(dytest,ytest_pred))
            eval_rec[i,j]=log_loss(dytest,ytest_pred)
            
        blend_train[:,5*j:5*j+5]=blend_temp
        blend_sub[:,5*j:5*j+5]=blend_sub_temp/float(nf)
        
np.savetxt("dog_blend_train7_2.txt",blend_train) 
np.savetxt("dog_blend_pred7_2.txt",blend_sub) 
np.savetxt("dy7_2.txt",dy)

etime = float(time.time()-stime)