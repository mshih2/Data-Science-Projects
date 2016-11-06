import pandas as pd
import xgboost as xgb
import time
from sklearn.cross_validation import ShuffleSplit
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle

stime = time.time()

o=[30,462,523,632,968,970, 1298, 1324]
train=pd.read_csv('./train-c.csv',index_col=0)
target=np.log(pd.read_csv('./target.csv',index_col=0, header=None).astype('float64'))

train=train.drop(o,axis=0)
target=target.drop(o,axis=0)

train.index=range(0,train.shape[0])
target.index=range(0,train.shape[0])

n=8000

### XGB pred model
est=xgb.XGBRegressor(colsample_bytree=0.91653966400601061,
                 gamma=0.014010492639853843,                 
                 learning_rate=0.02934991712918996,
                 max_depth=18,
                 min_child_weight=1.9231824156416961,
                 n_estimators=404,                                                                    
                 reg_alpha=0.30112133879436787,
                 reg_lambda=0.54300179573419061,
                 subsample=0.48538983247380996)


#crossvalidate the scores on a number of different random splits of the data

scores=pd.DataFrame(np.zeros([n,train.shape[1]]))
scores.columns=train.columns
ct=0

for train_idx, test_idx in ShuffleSplit(train.shape[0], n, .25):
    ct+=1
    print ("Iteration " + str(ct)+ " Start")
    X_train, X_test = train.ix[train_idx,:], train.ix[test_idx,:]
    Y_train, Y_test = target.ix[train_idx], target.ix[test_idx]
    r = est.fit(X_train, Y_train)
    acc = mean_squared_error(Y_test, est.predict(X_test))
    for i in range(train.shape[1]):
        X_t = X_test.copy()
        X_t.ix[:,i]=shuffle(np.array(X_t.ix[:, i]))
        shuff_acc =  mean_squared_error(Y_test, est.predict(X_t))
        scores.ix[ct-1,i]=((acc-shuff_acc)/acc)

fin_score=pd.DataFrame(np.zeros([train.shape[1],4]))
fin_score.columns=['Mean','Median','Max','Min']
fin_score.index=train.columns
fin_score.ix[:,0]=scores.mean()
fin_score.ix[:,1]=scores.median()
fin_score.ix[:,2]=scores.min()
fin_score.ix[:,3]=scores.max()

fin_score.to_csv('feature_importances.csv')

etime = float(time.time()-stime)