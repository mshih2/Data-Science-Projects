import numpy as np
import pandas as pd
import xgboost as xgb
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

stime = time.time()

train=pd.read_csv('./train-b.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))

### XGB CV model
def xgbcv(
           max_depth, 
          learning_rate, 
          n_estimators,
          min_child_weight,
          gamma,
          subsample,
          colsample_bytree,
          reg_alpha, 
          reg_lambda,          
          silent=True):
    return cv_s(xgb.XGBRegressor(
                                             max_depth=int(max_depth),
                                             learning_rate=learning_rate,
                                             n_estimators=int(n_estimators),
                                             silent=silent,
                                             gamma=gamma,
                                             min_child_weight=min_child_weight,
                                             subsample=subsample,
                                             colsample_bytree=colsample_bytree,
                                             reg_alpha=reg_alpha,
                                             reg_lambda=reg_lambda),
                    train,
                    target,
                    "mean_squared_error",
                    cv=4).mean()
                                 
xgboostBO = BayesOpt(xgbcv,
                                 {
                                  'max_depth': (4,25),
                                  'learning_rate': (0.01, 0.2),
                                  'n_estimators': (200,500),
                                  'gamma': (0.01, 1),
                                  'min_child_weight': (1,10),
                                  'subsample': (0.2, 1),
                                  'colsample_bytree' :(0.2, 1),
                                  'reg_alpha':(0, 1),
                                  'reg_lambda':(0, 1)
                                  })

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=50,n_iter=250, xi=0.05,  acq="poi")
xgboostBO.res["max"]

#{'max_params': {'colsample_bytree': 0.4783031566144188,
#  'gamma': 0.042639182720176985,
#  'learning_rate': 0.066763078898731051,
#  'max_depth': 13.493302378496974,
#  'min_child_weight': 6.6524305773262276,
#  'n_estimators': 344.27848632722362,
#  'reg_alpha': 0.49750276799063642,
#  'reg_lambda': 0.5949908091433086,
#  'subsample': 0.94020424847283524},
# 'max_val': -0.015731338120533046}


etime = float(time.time()-stime)