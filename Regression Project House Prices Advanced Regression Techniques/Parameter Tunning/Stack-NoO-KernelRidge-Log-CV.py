import numpy as np
import pandas as pd
from sklearn.kernel_ridge import KernelRidge
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

stime = time.time()
o=[30,88,462,523,632,691,968,970,1182,1324]
train=pd.read_csv('./blend_train_combined.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))
LO_features=pd.read_csv('./L-sec-features.csv',index_col=None, header=None)

train=train.ix[:,LO_features.ix[:,0]]

#train=train.drop(o,axis=0)
target=target.drop(o,axis=0)

#train.index=range(0,train.shape[0])
target.index=range(0,target.shape[0])
### XGB CV model
def Kernelcv(
          alpha, 
          gamma):
    return cv_s(KernelRidge(
                            alpha=10**alpha,
                            gamma=10**gamma,
                            kernel='rbf'
                            ),
                    train,
                    target,
                    "mean_squared_error",
                    cv=15).mean()
                                 
xgboostBO = BayesOpt(Kernelcv,
                                 {
                                  'alpha': (-4,0),
                                  'gamma': (-4,0)
                                  })

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=50,n_iter=350, xi=0.05,  acq="poi")
xgboostBO.res["max"]

#{'max_params': {'alpha': -11.987134249547031, 'gamma': -10.121297527127235},
# 'max_val': -0.008560592224131967}
 
etime = float(time.time()-stime)