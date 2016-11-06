import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
import time


stime = time.time()


train=pd.read_csv('./train-m.csv',index_col=0)
test=pd.read_csv('./test-m.csv',index_col=0)
#train=pd.read_csv('./train-b.csv',index_col=0)
#test=pd.read_csv('./test-b.csv',index_col=0)
#train=pd.read_csv('./blend_train_sec_No.csv',index_col=0)
#test=pd.read_csv('./blend_pred_sec_No.csv',index_col=0)
target=pd.read_csv('./target.csv',index_col=0, header=None).astype('float64')
submission=pd.read_csv('./sample_submission.csv')


est=Lasso(alpha=10**(-3.3424856865435171),max_iter=3000)

est.fit(train,target) 
pred=est.predict(test)

submission['SalePrice']=np.exp(pred)
submission.to_csv('output.csv',index=False)

coefs=est.coef_
features=pd.Series(train.columns[np.absolute(coefs)!=0])
features.to_csv('./L-features.csv',index=False)



etime = float(time.time()-stime)