# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 22:44:58 2016

@author: meichengshih
"""
import pandas as pd
import xgboost as xgb
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

train=pd.read_csv('./train-c.csv',index_col=0)
test=pd.read_csv('./test-c.csv',index_col=0)
target=pd.read_csv('./target.csv',index_col=0)

alldata=pd.concat([train,test],axis=0,ignore_index=True)
areacol=['latitude','longitude','gps_height']
gpstrain=alldata.ix[alldata['gps_height']!=0,areacol]
gpstest=alldata.ix[alldata['gps_height']==0,areacol]
height=alldata.ix[alldata['gps_height']!=0,'gps_height']
gpstrain=gpstrain.drop(['gps_height'],axis=1)
gpstest=gpstest.drop(['gps_height'],axis=1)

def xgbcv(max_depth, 
          learning_rate, 
          n_estimators,
          min_child_weight,
          gamma,
          reg_alpha,
          subsample=1,
          colsample_bytree=1,
          silent=True):
    return cv_s(xgb.XGBRegressor(max_depth=int(max_depth),
                                 learning_rate=learning_rate,
                                 n_estimators=int(n_estimators),
                                 gamma=gamma,
                                 reg_alpha=reg_alpha,
                                 min_child_weight=min_child_weight,
                                 objective='reg:linear'),
                    gpstrain,
                    height,
                    "mean_squared_error",
                    cv=4).mean() 
## can optimize std
xgboostBO = BayesOpt(xgbcv,
                                 {
                                  'max_depth': (8,17),
                                  'learning_rate': (0.01, 0.1),
                                  'n_estimators': (100,500),
                                  'reg_alpha':(0,1),
                                  'gamma': (0.1, 1),
                                  'min_child_weight': (0,10),
                                  })                                

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=10,n_iter=110, xi=0.0,  acq="poi")                            
