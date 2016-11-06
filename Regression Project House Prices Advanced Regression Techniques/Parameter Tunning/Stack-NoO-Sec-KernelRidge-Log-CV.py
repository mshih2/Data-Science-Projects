import numpy as np
import pandas as pd
from sklearn.kernel_ridge import KernelRidge
import time
from sklearn.cross_validation import cross_val_score as cv_s
from bayes_opt import BayesianOptimization as BayesOpt

stime = time.time()

o=[30,462,495,523,632,970, 1289,1324]
traindata=pd.read_csv('./blend_train.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))
nf=50

#traindata=traindata.drop(o,axis=0)
#target=target.drop(o,axis=0)

#traindata.index=range(0,traindata.shape[0])
#target.index=range(0,traindata.shape[0])

#traindata=traindata.ix[:,L_features.ix[:,0]]

### XGB CV model
def Kernelcv(
          alpha, 
          gamma):
    return -((-cv_s(KernelRidge(
                            alpha=10**alpha,
                            gamma=10**gamma,
                            kernel='rbf'
                            ),
                    traindata,
                    target,
                    "mean_squared_error",
                    cv=10).mean())**0.5)
                                 
xgboostBO = BayesOpt(Kernelcv,
                                 {
                                  'alpha': (-2, -1),
                                  'gamma': (-2, -1)
                                  })

print ("Start Optimization of Main Model")
xgboostBO.maximize(init_points=50,n_iter=350, xi=0.05,  acq="poi")
xgboostBO.res["max"]

#{'max_params': {'alpha': -2.3405748356840319, 'gamma': -0.95995274293421018},
# 'max_val': -0.010021231086057682}

# 500-15-no
#{'max_params': {'alpha': -11.794465355319215, 'gamma': -9.6130228126748882},
# 'max_val': -0.010009470913376273}

# 500-15-no-more
#{'max_params': {'alpha': -11.837378408540506, 'gamma': -9.1153909839966953},

# 500-15-no-no-more
#{'max_params': {'alpha': -11.667801825030947, 'gamma': -11.41429591954439},
# 'max_val': -0.010128587052329946}

#{'max_params': {'alpha': -11.980144349021876, 'gamma': -11.829983125206892},
# 'max_val': -0.014522232562068646}

#{'max_params': {'alpha': -12.36927188035942, 'gamma': -9.2371399762089759},
# 'max_val': -0.0086780619516334812}


etime = float(time.time()-stime)