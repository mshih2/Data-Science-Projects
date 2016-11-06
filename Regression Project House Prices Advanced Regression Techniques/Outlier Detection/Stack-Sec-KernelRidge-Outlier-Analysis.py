import numpy as np
import pandas as pd
from sklearn.kernel_ridge import KernelRidge
import time
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import statsmodels.api as sm

stime = time.time()

#o=[30,88,410,462,495,523,588,632,688,691,812,825,916,968,970,1182, 1324,1432,1453]
train=pd.read_csv('./blend_train_sec_v2.csv',index_col=0)
test=pd.read_csv('./blend_pred_sec_v2.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))
submission=pd.read_csv('./sample_submission.csv')

#traindata=traindata.drop(o,axis=0)
#target=target.drop(o,axis=0)

#traindata.index=range(0,traindata.shape[0])
#target.index=range(0,target.shape[0])

### XGB CV model
est=KernelRidge(alpha=10**(-5.5503364612798975),
            gamma=10**(-6.2892923234964915),
            kernel='rbf')

est.fit(train,target) 

predtrain=est.predict(train)
pred=est.predict(test)

k=pd.concat([target,pd.DataFrame(predtrain)],axis=1)
k.columns=['target','pred']
k=k.sort_values(['target'],axis=0) 

#{'max_params': {'alpha': -5.8517003633210605, 'gamma': -6.152588757748549},
# 'max_val': -0.014113663783087149}

#{'max_params': {'alpha': -7.4327217408144799, 'gamma': -3.4283633381920602},
# 'max_val': -0.01005850858552319}

#{'max_params': {'alpha': -11.980144349021876, 'gamma': -11.829983125206892},
# 'max_val': -0.014522232562068646}

plt.scatter(np.exp(predtrain), np.exp(target))
plt.plot([min(np.exp(predtrain)),max(np.exp(predtrain))], [min(np.exp(target)),max(np.exp(target))], ls="--", c=".3")
plt.xlim([0,800000])
plt.ylim([0,800000])
plt.xlabel("Prediction")
plt.ylabel("Ground Truth")
print (r2_score(np.exp(predtrain), np.exp(target)))

results = sm.OLS(target, predtrain).fit()
outliertest=results.outlier_test(method='bonf', alpha=0.01)
pos_out=outliertest.ix[outliertest['bonf(p)']<1,:]
pos_point=np.where(outliertest['bonf(p)']<1)

pos_out.to_csv('influence.csv')

etime = float(time.time()-stime)