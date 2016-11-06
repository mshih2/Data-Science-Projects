import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
import time
from sklearn.cross_validation import cross_val_score as cv_s

stime = time.time()

train=pd.read_csv('./train-b.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))

### XGB CV model
def KNNcv(n_neighbors):
    return cv_s(KNeighborsRegressor(
           n_neighbors=int(n_neighbors), 
           weights='distance', 
           algorithm='brute',
           metric='cosine'),
                    train,
                    target,
                    "mean_squared_error",
                    cv=15).mean()
                                 
for i in xrange(40):
    print(i+1,KNNcv(i+1))
    if i==0:
        opt_n=i
        opt_mse= KNNcv(i+1) 
    
    else:    
        if KNNcv(i+1)>opt_mse:
            opt_n=i
            opt_mse= KNNcv(i+1)
    
print ("Optimal count and result")    
print (opt_n, opt_mse)


#(9, -0.038296260512139399)

#v2
#(9, -0.038128352384478342)


etime = float(time.time()-stime)