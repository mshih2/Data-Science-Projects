# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:35:39 2016

@author: meichengshih
"""
import pandas as pd
import numpy as np
from sklearn.kernel_ridge import KernelRidge
import xgboost as xgb
import time
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import KFold

stime = time.time()

#o=[30,410,462,495,523,588,632,688,968,970, 1298,1324,1432]
traindata=pd.read_csv('./blend_train_sec_No.csv',index_col=0)
testdata=pd.read_csv('./blend_pred_sec_No.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))
submission=pd.read_csv('./sample_submission.csv')
nf=500

#train=train.drop(o,axis=0)
#target=target.drop(o,axis=0)

#train.index=range(0,train.shape[0])
#target.index=range(0,traindata.shape[0])

############ Start ################

## Normal Models
# trainc,target             
cclf1=xgb.XGBRegressor(
                 gamma= 0.022700481549776746,                 
                 learning_rate=0.05542400679411822,
                 max_depth=9,
                 min_child_weight=9.4978897696896105,
                 n_estimators=518,                                                                    
                 reg_alpha= 0.72866976949421347,
                 reg_lambda=9.3224954905632895)

## 50
#{'max_params': {'gamma': 0.12957031369056071,
#  'learning_rate': 0.10161638656225325,
#  'max_depth': 14.773519842447916,
#  'min_child_weight': 23.411825988768367,
#  'n_estimators': 208.20603961058922,
#  'reg_alpha': 0.38118924525951292,
#  'reg_lambda': 0.0068700920532802634},
# 'max_val': -0.015058700043690141}
           
               
# trainb ,target
cclf2=KernelRidge(alpha=10**(-3.8272220639957997),
            gamma=10**(-0.01339916145757061),
            kernel='rbf')
## 50-15
#{'max_params': {'alpha': -2.2568941196877219, 'gamma': -1.9284382171852981},
# 'max_val': -0.013657552495021551}                          


cclfs=[cclf1, cclf2]

## KFold
print ("Start Stacking Models")
eval_rec=pd.DataFrame(np.zeros((nf,len(cclfs))))
blend_temp=pd.DataFrame(np.zeros((traindata.shape[0],1)))
blend_sub_temp=pd.DataFrame(np.zeros((testdata.shape[0],1)))
blend_train=pd.DataFrame(np.zeros((traindata.shape[0],len(cclfs))))
blend_sub=pd.DataFrame(np.zeros((testdata.shape[0],len(cclfs))))

for j, clf in enumerate(cclfs):
    print (str(j+1)+"th Regressor")
    ### K-Fold with Shufffle
    skf = list(KFold(len(target), nf ,shuffle=True))
    for i in xrange(nf):
        train, test=skf[i]
        xtrain, xtest = traindata.ix[train,:], traindata.ix[test,:]
        ytrain, ytest = target.ix[train], target.ix[test]
        ytrain =ytrain.ix[:,1]
        clf.fit(xtrain, ytrain)
        ytest_pred = clf.predict(xtest).astype('float32')
        blend_temp.ix[test,0]=ytest_pred
        sub_pred = pd.DataFrame(clf.predict(testdata)).astype('float32')
        ### Record    
        if i==0:
            blend_sub_temp=sub_pred
        else:
            blend_sub_temp=blend_sub_temp+sub_pred
                
        print (i, mean_squared_error(ytest,ytest_pred), (time.time()-stime))
        eval_rec.ix[i,j]=mean_squared_error(ytest,ytest_pred)
        
    blend_train.ix[:,j]=blend_temp.ix[:,0]
    blend_sub.ix[:,j]=blend_sub_temp.ix[:,0]/float(nf)
        
blend_train.to_csv("blend_train_sec_v2.csv", index_label=False)
blend_sub.to_csv("blend_pred_sec_v2.csv", index_label=False)  


etime = float(time.time()-stime)