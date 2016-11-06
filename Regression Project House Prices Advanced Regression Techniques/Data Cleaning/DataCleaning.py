# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 20:54:52 2016

@author: meichengshih
"""
from scipy.stats import mode
import pandas as pd
import numpy as np
import time
from scipy.stats import skew
import statsmodels.api as sm

stime = time.time()

"""
Read Data
"""
train=pd.read_csv('./train.csv')
test=pd.read_csv('./test.csv')
target=np.log(train['SalePrice'])
train=train.drop(['SalePrice'],axis=1)
trainlen=train.shape[0]

## Combined data to train
alldata=pd.concat([train, test], axis=0, join='outer',ignore_index=True)
alldata=alldata.drop(['Id','Utilities'],axis=1)
alldata['MSSubClass']=alldata['MSSubClass'].astype('object')
alldata['LotArea']=alldata['LotArea'].astype('float64')
alldata['YearBuilt']=alldata['YearBuilt'].astype('float64')
alldata['YearRemodAdd']=alldata['YearRemodAdd'].astype('float64')
alldata['GrLivArea']=alldata['GrLivArea'].astype('float64')
alldata['1stFlrSF']=alldata['1stFlrSF'].astype('float64')
alldata['2ndFlrSF']=alldata['2ndFlrSF'].astype('float64')
alldata['LowQualFinSF']=alldata['LowQualFinSF'].astype('float64')
alldata['WoodDeckSF']=alldata['WoodDeckSF'].astype('float64')
alldata['OpenPorchSF']=alldata['OpenPorchSF'].astype('float64')
alldata['3SsnPorch']=alldata['3SsnPorch'].astype('float64')
alldata['ScreenPorch']=alldata['ScreenPorch'].astype('float64')
alldata['PoolArea']=alldata['PoolArea'].astype('float64')
alldata['MoSold']=alldata['MoSold'].astype('float64')
alldata['YrSold']=alldata['YrSold'].astype('float64')
alldata['MiscVal']=alldata['MiscVal'].astype('float64')

### Skewed variables
numeric_feats = alldata.dtypes[(alldata.dtypes=='float64')].index
skewed_feats = train[numeric_feats].apply(lambda x: skew(x.dropna()))
skewed_feats = skewed_feats[np.absolute(skewed_feats) > 0.8]
skewed_feats = skewed_feats.index

alldata[skewed_feats] = np.log1p(alldata[skewed_feats])

## Deal with the LotFrontage and LotArea
x = alldata.ix[alldata["LotFrontage"].notnull(), "LotArea"]
y = alldata.ix[alldata["LotFrontage"].notnull(), "LotFrontage"]
#### From Skeweness test, found that both x and y are skewed variables
x= sm.add_constant(x)
model=sm.OLS(y,x)
results=model.fit()
#### Find outlier of x and y
out_test=results.outlier_test()
ok_p=out_test['bonf(p)']>0.5
x=x.ix[ok_p,:]
y=y.ix[ok_p]
### Do regression without outliers
model=sm.OLS(y,x)
results2=model.fit()
alldata.ix[alldata["LotFrontage"].isnull(), "LotFrontage"]=results2.params[0]+results2.params[1]*alldata["LotArea"]

### replace the nans
alldata.ix[alldata.Alley.isnull(), 'Alley'] = 'NoAlley'
alldata.ix[alldata.MasVnrType.isnull(), 'MasVnrType'] = 'None' # no good
alldata.ix[alldata.MasVnrType == 'None', 'MasVnrArea'] = 0
## checked the only row 2120
alldata.ix[alldata.TotalBsmtSF.isnull(), 'TotalBsmtSF'] = 0
alldata.ix[alldata['TotalBsmtSF']==0, 'BsmtCond'] = 'NoBsmt'
alldata.ix[alldata['TotalBsmtSF']==0, 'BsmtQual'] = 'NoBsmt'
alldata.ix[alldata['TotalBsmtSF']==0, 'BsmtExposure'] = 'NoBsmt'
alldata.ix[alldata['TotalBsmtSF']==0, 'BsmtFinType1'] = 'NoBsmt'
alldata.ix[alldata['TotalBsmtSF']==0, 'BsmtFinType2'] = 'NoBsmt'
alldata.ix[alldata.BsmtCond.isnull(), 'BsmtCond'] = alldata.BsmtCond.mode()[0]
alldata.ix[alldata.BsmtQual.isnull(), 'BsmtQual'] = alldata.BsmtQual.mode()[0]
alldata.ix[alldata.BsmtExposure.isnull(), 'BsmtExposure'] = alldata.BsmtExposure.mode()[0]
alldata.ix[alldata.BsmtFinType1.isnull(), 'BsmtFinType1'] = alldata.BsmtFinType1.mode()[0]
alldata.ix[alldata.BsmtFinType2.isnull(), 'BsmtFinType2'] = alldata.BsmtFinType2.mode()[0]
alldata.ix[alldata.BsmtFinType1=='NoBsmt', 'BsmtFinSF1'] = 0
alldata.ix[alldata.BsmtFinSF1.isnull(), 'BsmtFinSF1'] = alldata.BsmtFinSF1.median()
alldata.ix[alldata.BsmtFinType2=='NoBsmt', 'BsmtFinSF2'] = 0
alldata.ix[alldata.BsmtUnfSF.isnull(), 'BsmtUnfSF'] = alldata.BsmtUnfSF.median()


Bsmtlist=['BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2','BsmtFinSF1','BsmtFinSF2','BsmtUnfSF']

### Fireplace
alldata.ix[alldata['Fireplaces']==0, 'FireplaceQu'] = 'NoFireplace'

### Garage
Garagelist=['GarageArea','GarageCars','GarageType','GarageYrBlt','GarageFinish','GarageQual','GarageCond']

alldata.ix[alldata.GarageArea.isnull(), 'GarageArea'] = 0
alldata.ix[alldata.GarageCars.isnull(), 'GarageCars'] = 0
alldata.ix[(alldata.GarageFinish.isnull()) & (alldata['GarageArea']>0), 'GarageFinish'] = alldata.GarageFinish.mode()[0]
alldata.ix[(alldata.GarageQual.isnull()) & (alldata['GarageArea']>0), 'GarageQual'] = alldata.GarageQual.mode()[0]
alldata.ix[(alldata.GarageCond.isnull()) & (alldata['GarageArea']>0), 'GarageCond'] = alldata.GarageCond.mode()[0]
alldata.ix[(alldata.GarageYrBlt.isnull()) & (alldata['GarageArea']>0), 'GarageYrBlt'] = alldata.GarageYrBlt.median()
alldata.ix[alldata.GarageFinish.isnull(), 'GarageFinish'] = 'NoGarage'
alldata.ix[alldata.GarageQual.isnull(), 'GarageQual'] = 'NoGarage'
alldata.ix[alldata.GarageCond.isnull(), 'GarageCond'] = 'NoGarage'
alldata.ix[alldata.GarageYrBlt.isnull(), 'GarageYrBlt'] = alldata.GarageYrBlt.median()
alldata.ix[alldata.GarageType.isnull(), 'GarageType'] = 'NoGarage'

### checked with BsmtArea
alldata.ix[alldata.BsmtFullBath.isnull(), 'BsmtFullBath'] = 0
alldata.ix[alldata.BsmtHalfBath.isnull(), 'BsmtHalfBath'] = 0

### Pool
alldata.ix[alldata['PoolArea']==0, 'PoolQC'] = 'NoPool'
alldata.ix[(alldata['PoolArea']>0) &((alldata['PoolQC']=='NoPool') | alldata['PoolQC'].isnull()), 'PoolQC'] = alldata.PoolQC.mode()[0]
alldata.ix[alldata['PoolQC'].isnull(), 'PoolQC'] = 'NoPool'

### Others
alldata.ix[alldata['Fence'].isnull(), 'Fence'] = 'NoFence'
alldata.ix[alldata['MiscFeature'].isnull(), 'MiscFeature'] = 'None'
alldata.ix[alldata['Electrical'].isnull(), 'Electrical'] = alldata.Electrical.mode()[0]
alldata.ix[alldata.KitchenQual.isnull(), 'KitchenQual'] = alldata.KitchenQual.mode()[0]
alldata.ix[alldata.MSZoning.isnull(), 'MSZoning'] = alldata.MSZoning.mode()[0]
alldata.ix[alldata.Exterior1st.isnull(), 'Exterior1st'] = alldata.Exterior1st.mode()[0]
alldata.ix[alldata.Exterior2nd.isnull(), 'Exterior2nd'] = alldata.Exterior2nd.mode()[0]
alldata.ix[alldata.Functional.isnull(), 'Functional'] = alldata.Functional.mode()[0]
alldata.ix[alldata.SaleCondition.isnull(), 'SaleCondition'] = alldata.SaleCondition.mode()[0]
alldata.ix[alldata.SaleType.isnull(), 'SaleType'] = alldata.SaleType.mode()[0]

ordinallist=['Street', 'FireplaceQu','Fence','ExterQual','BsmtQual','BsmtExposure','BsmtCond',
            'GarageQual','KitchenQual','Functional','CentralAir','PavedDrive']

alldata = alldata.replace({'Street': {'Pave': 1, 'Grvl': 0 },
                             'FireplaceQu': {'Ex': 5, 
                                            'Gd': 4, 
                                            'TA': 3, 
                                            'Fa': 2,
                                            'Po': 1,
                                            'NoFireplace': 0 
                                            },
                             'Fence': {'GdPrv': 2, 
                                       'GdWo': 2, 
                                       'MnPrv': 1, 
                                       'MnWw': 1,
                                       'NoFence': 0},
                             'ExterQual': {'Ex': 5, 
                                            'Gd': 4, 
                                            'TA': 3, 
                                            'Fa': 2,
                                            'Po': 1
                                            },
                             'ExterCond': {'Ex': 5, 
                                            'Gd': 4, 
                                            'TA': 3, 
                                            'Fa': 2,
                                            'Po': 1
                                            },
                             'BsmtQual': {'Ex': 5, 
                                            'Gd': 4, 
                                            'TA': 3, 
                                            'Fa': 2,
                                            'Po': 1,
                                            'NoBsmt': 0,
                                            'NA':-1},
                             'BsmtExposure': {'Gd': 3, 
                                            'Av': 2, 
                                            'Mn': 1,
                                            'No': 0,
                                            'NoBsmt': 0},
                             'BsmtCond': {'Ex': 5, 
                                            'Gd': 4, 
                                            'TA': 3, 
                                            'Fa': 2,
                                            'Po': 1,
                                            'NoBsmt': 0},
                             'GarageQual': {'Ex': 5, 
                                            'Gd': 4, 
                                            'TA': 3, 
                                            'Fa': 2,
                                            'Po': 1,
                                            'NoGarage': 0},
                             'GarageCond': {'Ex': 5, 
                                            'Gd': 4, 
                                            'TA': 3, 
                                            'Fa': 2,
                                            'Po': 1,
                                            'NoGarage': 0},
                             'PoolQC': {'Ex': 3, 
                                            'Gd': 2, 
                                            'Fa': 1, 
                                            'NoPool': 0},                                            
                             'KitchenQual': {'Ex': 5, 
                                            'Gd': 4, 
                                            'TA': 3, 
                                            'Fa': 2,
                                            'Po': 1},
                            'HeatingQC': {'Ex': 5, 
                                            'Gd': 4, 
                                            'TA': 3, 
                                            'Fa': 2,
                                            'Po': 1},
                             'Functional': {'Typ': 0,
                                            'Min1': 1,
                                            'Min2': 1,
                                            'Mod': 2,
                                            'Maj1': 3,
                                            'Maj2': 4,
                                            'Sev': 5,
                                            'Sal': 6}                             
                            })
alldata = alldata.replace({'CentralAir': {'Y': 1, 
                                            'N': 0}})
alldata = alldata.replace({'PavedDrive': {'Y': 1, 
                                            'P': 0,
                                            'N': 0}})


alldata[ordinallist]=alldata[ordinallist].astype('float64')                                           

alldata = pd.get_dummies(alldata)

for i in xrange(alldata.shape[1]):
    alldata.ix[:,i]=alldata.ix[:,i].astype('float64')

#alldata -= alldata.min()
#alldata /= alldata.max()-alldata.min()

train=alldata.ix[0:trainlen-1,:]
test=alldata.ix[trainlen:alldata.shape[0],:]

train.to_csv('train-m.csv', index_label=False)
test.to_csv('test-m.csv', index_label=False)
target.to_csv('target.csv', index_label=False)

etime = float(time.time()-stime)