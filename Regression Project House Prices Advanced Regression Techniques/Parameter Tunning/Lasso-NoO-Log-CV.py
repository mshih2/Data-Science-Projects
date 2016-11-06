import pandas as pd
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt
import numpy as np
from sklearn.linear_model import Lasso

stime = time.time()

#o=[30,410,462,495,523,588,632,688,968,970, 1298,1324,1432]
train=pd.read_csv('./train-b.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))

#train=train.drop(o,axis=0)
#target=target.drop(o,axis=0)

#train.index=range(0,train.shape[0])
#target.index=range(0,train.shape[0])

### XGB CV model
def Kernelcv(
          alpha):
    return cv_s(Lasso(
                            alpha=10**alpha
                            ),
                    train,
                    target,
                    "mean_squared_error",
                    cv=4).mean()
                                 
xgboostBO = BayesOpt(Kernelcv,
                                 {
                                  'alpha': (-3.3, -3.2)
                                  })

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=50,n_iter=250, xi=0.05,  acq="poi")
xgboostBO.res["max"]

# no outliers
#{'max_params': {'alpha': -3.6392536392421784},
# 'max_val': -0.0099399944646872615}

# outliers
#{'max_params': {'alpha': -3.2868282025067179},
# 'max_val': -0.015103465103503494}
 
etime = float(time.time()-stime)