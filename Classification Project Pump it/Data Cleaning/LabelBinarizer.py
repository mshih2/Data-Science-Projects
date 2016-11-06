# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 11:01:52 2016

@author: meichengshih
"""

from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import time

stime = time.time()

train=pd.read_csv('./train-c.csv',index_col=0)
test=pd.read_csv('./test-c.csv',index_col=0)
target=pd.read_csv('./target.csv',index_col=0)


train_c=np.array(train.ix[:,train.dtypes=='int64'])
train_n=np.array(train.ix[:,train.dtypes=='float64'])
trainum=train.shape[0]

test_c=np.array(test.ix[:,test.dtypes=='int64'])
test_n=np.array(test.ix[:,test.dtypes=='float64'])

all_c=np.concatenate((train_c,test_c),axis=0)

enc=OneHotEncoder()
all_c=enc.fit_transform(all_c).toarray()

train=np.concatenate((all_c[0:trainum,:],train_n),axis=1)
test=np.concatenate((all_c[trainum:all_c.shape[0],:],test_n),axis=1)

del(all_c, test_c, train_c, train_n, test_n)

pd.DataFrame(train).to_hdf('train_b.h5','w')
pd.DataFrame(test).to_hdf('test_b.h5','w')

etime = float(time.time()-stime)