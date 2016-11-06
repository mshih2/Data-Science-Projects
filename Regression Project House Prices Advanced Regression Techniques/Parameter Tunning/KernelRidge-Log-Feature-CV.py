import numpy as np
import pandas as pd
from sklearn.kernel_ridge import KernelRidge
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

#o=[30,410,462,495,523,588,632,688,968,970, 1298,1324,1432]
stime = time.time()
train=pd.read_csv('./train-m.csv',index_col=0)
target=pd.read_csv('./target.csv',index_col=0, header=None).astype('float64')
features=pd.read_csv('./L-features.csv',index_col=False, header=None)

#train=train.drop(o,axis=0)
#target=target.drop(o,axis=0)

#train.index=range(0,train.shape[0])
#target.index=range(0,train.shape[0])

train=train.ix[:,np.where(train.columns==features)[1]]


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
                    cv=4).mean()
                                 
xgboostBO = BayesOpt(Kernelcv,
                                 {
                                  'alpha': (-8,0),
                                  'gamma': (-8,0)
                                  })

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=50,n_iter=350, xi=0.05,  acq="poi")
xgboostBO.res["max"]

#{'max_params': {'alpha': -2.3534935983173315, 'gamma': -2.5598522482339896},
# 'max_val': -0.014045783322961644}


etime = float(time.time()-stime)