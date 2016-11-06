# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 14:01:20 2016

@author: meichengshih
"""

import pandas as pd
from sklearn.preprocessing import RobustScaler
import numpy as np


data=pd.read_csv('output.csv', header=0, index_col=0)


#### Data Cleaning
def Cleaning(data):
## Construct Feature Matrix
    features=data.drop('Delay_100_Mile',axis=1)
#    target=np.log1p(data['Delay_100_Mile'])
    target=data['Delay_100_Mile']
    ct=features.shape[1]
    var_num=features.shape[1]
    columns=features.columns
    for i in range(0,var_num):
        for j in range(i,var_num):
            features.insert(ct,str(columns[i])+'_'+str(columns[j]),features[columns[i]]*features[columns[j]])
            ct+=1

    ## Rescale the Features
    robust_scaler = RobustScaler()
    columns=features.columns
    features = robust_scaler.fit_transform(features)
    features = pd.DataFrame(features, columns=columns)
    data=pd.concat([features,target],axis=1)
    data.index=pd.DataFrame(data.groupby(by=['TC','ATP','IP']).grouper.group_info[0])    
    return data

#### Cross Validation of Quantile Regression
def quantCV(q,alpha,L1_wt,data,folds):
    import statsmodels.formula.api as smf
#    from statsmodels.regression.quantile_regression import QuantReg
    from sklearn.cross_validation import KFold
    from sklearn.metrics import mean_squared_error as MSE
    import warnings
    warnings.filterwarnings("ignore")

## KFold
    kf = KFold(len(np.unique(data.index)), n_folds=folds, random_state=0)
    score=np.zeros(folds)
    ct=0
## Train Model
    for train_index, test_index in kf:
        data_train=data[np.array(pd.DataFrame(data.index).isin(train_index).values.tolist())]
        data_test=data[np.array(pd.DataFrame(data.index).isin(test_index).values.tolist())]
        mod = smf.quantreg('Delay_100_Mile ~ TC + ATP + IP + TC_TC + TC_ATP + TC_IP + ATP_ATP + ATP_IP + IP_IP',data_train)
        res = mod.fit_regularized(q=q,alpha=alpha, L1_wt=L1_wt, maxiter=3000,random_state=0,cnvrg_tol=1e-08)

## Predict Values
        features_predict = data_test.groupby(by=['TC','ATP','IP'])[data.drop(['Delay_100_Mile'],axis=1).columns].mean()
        params = res.params
        delay_predicted = params[0]+np.dot(features_predict, params[1:])

## Corresponding Value of Same Percentile
        target_per=data_test.groupby(by=['TC','ATP','IP'])['Delay_100_Mile'].quantile(q)
#        score[ct]= MSE(np.expm1(target_per),np.expm1(delay_predicted))**.5
        score[ct]= MSE(target_per,delay_predicted)**.5
        ct+=1

    return np.mean(score)
    
#### Random Search
def simpleQuantRS(q,alpha_u,alpha_l,L1_u,L1_l,data,folds,n):
    record=np.zeros((n,3))
    for i in xrange(n):
        if i%10==0:
            print ('This is the '+str(i+1)+' th iterations of percentile '+str(q))
        alpha=np.round(10**(alpha_l+(alpha_u-alpha_l)*np.random.rand()),5)
        L1_wt=np.round(L1_l+(L1_u-L1_l)*np.random.rand(),5)
        record[i,0]=alpha
        record[i,1]=L1_wt
        record[i,2]=quantCV(q,alpha,L1_wt,data,folds)
    print (record[np.argmin(record[:,2]),:])    
    return record[np.argmin(record[:,2]),:]

        



#---------------------------- Main Porgram -----------------------------
data=Cleaning(data)
#qs=[.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,.6,.65,.7,.75,.8,.85,.9,.95]
qs=[.95]
ct=0
best_record=np.zeros((len(qs),3))
for q in qs:
    best_record[ct,:]=simpleQuantRS(q,1.5,-4,0.9,0.1,data,5,100)
    ct+=1
