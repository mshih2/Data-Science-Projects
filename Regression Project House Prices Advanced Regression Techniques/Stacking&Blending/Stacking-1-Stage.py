# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:35:39 2016

@author: meichengshih
"""
import pandas as pd
import numpy as np
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import Lasso
import xgboost as xgb
import time
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import KFold
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor

stime = time.time()

trainc=pd.read_csv('./train-m.csv',index_col=0)
testc=pd.read_csv('./test-m.csv',index_col=0)
target=pd.read_csv('./target.csv',index_col=0, header=None).astype('float64')
submission=pd.read_csv('./sample_submission.csv')
nf=500

############ Start ################

## Normal Models
# trainc,target             
cclf1=xgb.XGBRegressor(colsample_bytree=0.44799798156409804,
                 gamma=0.37620556986957449,                 
                 learning_rate=0.088254826083541099,
                 max_depth=6,
                 min_child_weight=2.2515633024248505,
                 n_estimators=345,                                                                    
                 reg_alpha=0.82446462821602562,
                 reg_lambda=0.118159209624777,
                 subsample=0.69055854570380215)
              
# trainb,target_norm
cclf2=BayesianRidge(n_iter=800, 
                    alpha_1=10**(-6.1201271979759895), 
                    alpha_2=10**(-7.9974198663160401), 
                    lambda_1=10**(-4.321607431874626), 
                    lambda_2=10**(-4.2957871570631454))

# check
cclf3=Lasso(alpha=10**(-4.2625417423330569))

# check
cclf4=KernelRidge(alpha=10**(-2.17549270755298),
            gamma=10**(-2.5327623991577588),
            kernel='rbf')  
#-0.015462336785988944

### LOG Models
# trainc, target
cclf5=xgb.XGBRegressor(colsample_bytree=0.72515318909290161,
                 gamma=0.082450843908748142,                 
                 learning_rate=0.10805405635347147,
                 max_depth=17,
                 min_child_weight=7.2425245194776666,
                 n_estimators=314,                                                                    
                 reg_alpha=0.11507490604527368,
                 reg_lambda=0.484445613042634,
                 subsample=0.48225028496214212)
                 #-0.012457832065225756

# check
cclf6=BayesianRidge(n_iter=800, 
                    alpha_1=10**(-4.4180920749661041), 
                    alpha_2=10**(-7.0430093666839744), 
                    lambda_1=10**(-6.9722456868194929), 
                    lambda_2=10**(-4.0043815601797785))
# -0.0018304166411495766                   

# check
cclf7=Lasso(alpha=10**(-1.8245923489234))  

# trainb, target
cclf8=KernelRidge(alpha=10**(-1.649913714013286),
            gamma=10**(-2.0956567812501579),
            kernel='rbf') 

cclf9=xgb.XGBRegressor(colsample_bytree=0.39395772492969583,
                 gamma=0.044343390506792514,                 
                 learning_rate=0.070828406729401647,
                 max_depth=20,
                 min_child_weight=1.495799071901752,
                 n_estimators=306,                                                                    
                 reg_alpha=0.66921403455226047,
                 reg_lambda=0.4689251309488115,
                 subsample=0.96886005118988527) 

cclf10=BayesianRidge(n_iter=800, 
                    alpha_1=10**(-6.6440446568101725), 
                    alpha_2=10**(-7.8110350173952732), 
                    lambda_1=10**(-6.8928405257226117), 
                    lambda_2=10**(-4.0301124829823536))

cclf11=KernelRidge(alpha=10**(-1.7735319312263793),
            gamma=10**(-2.2354138781662178),
            kernel='rbf')

cclf12=ExtraTreesRegressor(max_depth=19,
                                 max_features=0.86271169353866273,
                                 n_estimators=229,
                                 min_samples_leaf=1)
                                 #-0.019334066607660634

## XGB with onehotcoding
cclf13= xgb.XGBRegressor(colsample_bytree=0.4783031566144188,
                 gamma=0.042639182720176985,                 
                 learning_rate=0.066763078898731051,
                 max_depth=13,
                 min_child_weight=6.6524305773262276,
                 n_estimators=344,                                                                    
                 reg_alpha=0.49750276799063642,
                 reg_lambda=0.5949908091433086,
                 subsample=0.94020424847283524)                               

cclf14=RandomForestRegressor(max_depth=19,
                                 max_features=0.33670019282283797,
                                 n_estimators=440,
                                 min_samples_leaf=1)
                                 #-0.018970416840100559

cclf15=KernelRidge(alpha=10**(-1.477079682304058),
            gamma=10**(-2.2068605213186379),
            kernel='rbf')                            

cclfs=[cclf1, cclf2, cclf3, cclf4, cclf5, cclf6, cclf7, cclf8, cclf9, cclf10, cclf11,cclf12,cclf13,cclf14,cclf15]
trainset=[trainc,trainb,trainb,trainb,trainc,trainb,trainb,trainb,trainc, trainb,trainb,trainc,trainb,trainc,trainb]
testset=[testc,testb,testb,testb,testc,testb,testb,testb,testc,testb,testb,testc,testb,testc,testb]
targetset=[target,target_norm,target,target,target,target_norm,target,target,target,target_norm,target,target,target,target,target]
reverse=[False,True,False,False,False,True,False,False,False,True,False,False,False,False,False]


## KFold
print ("Start Stacking Models")
eval_rec=pd.DataFrame(np.zeros((nf,len(cclfs))))
blend_temp=pd.DataFrame(np.zeros((trainb.shape[0],1)))
blend_sub_temp=pd.DataFrame(np.zeros((testb.shape[0],1)))
blend_train=pd.DataFrame(np.zeros((trainb.shape[0],len(cclfs))))
blend_sub=pd.DataFrame(np.zeros((testb.shape[0],len(cclfs))))

for j, clf in enumerate(cclfs):
    print (str(j+1)+"th Regressor")
    ### K-Fold with Shufffle
    skf = list(KFold(len(targetset[j]), nf ,shuffle=True))
    for i in xrange(nf):
        train, test=skf[i]
        xtrain, xtest = trainset[j].ix[train,:], trainset[j].ix[test,:]
        ytrain, ytest = targetset[j].ix[train], targetset[j].ix[test]
        ytrain =ytrain.ix[:,1]
        clf.fit(xtrain, ytrain)
        ytest_pred = clf.predict(xtest).astype('float32')
        blend_temp.ix[test,0]=ytest_pred
        sub_pred = pd.DataFrame(clf.predict(testset[j])).astype('float32')
        ### Check Transformation
        if reverse[j]==True:
            ytest=      ytest*float(targetmax-targetmin)+targetmin
            ytest_pred= ytest_pred*float(targetmax-targetmin)+targetmin
            sub_pred=   sub_pred*float(targetmax-targetmin)+targetmin
        
        ### Record    
        if i==0:
            blend_sub_temp=sub_pred
        else:
            blend_sub_temp=blend_sub_temp+sub_pred
                
        print (i, mean_squared_error(ytest,ytest_pred), (time.time()-stime))
        eval_rec.ix[i,j]=mean_squared_error(ytest,ytest_pred)
        
    if reverse[j]==True:
        blend_temp= blend_temp*float(targetmax-targetmin)+targetmin
    blend_train.ix[:,j]=blend_temp.ix[:,0]
    blend_sub.ix[:,j]=blend_sub_temp.ix[:,0]/float(nf)
        
blend_train.to_csv("blend_train_log500-15-all.csv", index_label=False)
blend_sub.to_csv("blend_pred_log500-15-all.csv", index_label=False)  


etime = float(time.time()-stime)