import pandas as pd
from sklearn.linear_model import BayesianRidge
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt
import numpy as np

stime = time.time()

train=pd.read_csv('./train-b.csv',index_col=0)
target=pd.read_csv('./target.csv',index_col=0, header=None).astype('float64')
target=np.log(np.array(np.transpose(target.ix[:]))[0])
targetmin=min(target)
targetmax=max(target)
target=(target-targetmin)/(targetmax-targetmin)

### XGB CV model
def Kernelcv(
          alpha_1,
          alpha_2,
          lambda_1,
          lambda_2):
    return cv_s(BayesianRidge(n_iter=800, 
                    alpha_1=alpha_1, 
                    alpha_2=alpha_2, 
                    lambda_1=lambda_1, 
                    lambda_2=lambda_2
                            ),
                    train,
                    target,
                    "mean_squared_error",
                    cv=4).mean()
                                 
xgboostBO = BayesOpt(Kernelcv,
                                 {
                                  'alpha_1': (-8, -4),
                                  'alpha_2': (-8, -4),
                                  'lambda_1': (-8, -4),
                                  'lambda_2': (-8, -4)
                                  })

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=50,n_iter=250, xi=0.05,  acq="poi")
xgboostBO.res["max"]

#{'max_params': {'alpha_1': -5.8572336837097456,
#  'alpha_2': -7.7045215593126599,
#  'lambda_1': -4.7191989503901404,
#  'lambda_2': -4.0643295981217626},
# 'max_val': -0.0021668807816198196}

#{'max_params': {'alpha_1': -6.6440446568101725,
#  'alpha_2': -7.8110350173952732,
#  'lambda_1': -6.8928405257226117,
#  'lambda_2': -4.0301124829823536},
# 'max_val': -0.0021680393927769361}


etime = float(time.time()-stime)