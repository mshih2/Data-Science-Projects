import numpy as np
import pandas as pd
from sklearn.kernel_ridge import KernelRidge
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt
from sklearn.linear_model import Lasso

stime = time.time()

#o=[30,410,462,495,523,588,632,688,968,970, 1298,1324,1432]
traindata=pd.read_csv('./blend_train_feature.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))
nf=50

#traindata=traindata.drop(o,axis=0)
#target=target.drop(o,axis=0)

#traindata.index=range(0,traindata.shape[0])
#target.index=range(0,traindata.shape[0])

### XGB CV model
def Kernelcv(
          alpha):
    return cv_s(Lasso(
                            alpha=10**alpha
                            ),
                    traindata,
                    target,
                    "mean_squared_error",
                    cv=30).mean()
                                 
xgboostBO = BayesOpt(Kernelcv,
                                 {
                                  'alpha': (-13, -0.1)
                                  })

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=50,n_iter=350, xi=0.05,  acq="poi")
xgboostBO.res["max"]

#{'max_params': {'alpha': -4.3021424130219348},
# 'max_val': -0.0086766852987939756}


etime = float(time.time()-stime)