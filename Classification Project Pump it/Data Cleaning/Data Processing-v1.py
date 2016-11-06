# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 20:54:52 2016

@author: meichengshih
"""

import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder

stime = time.time()

"""
Read Data
"""
train=pd.read_csv('./train.csv')
test=pd.read_csv('./test.csv')
outcome=pd.read_csv('./outcome.csv')

## Merge all data and leave train num
trainum=train.shape[0]
alldata=pd.concat([train,test],axis=0,ignore_index=True)

### need to change scheme_name into small letters

## Drop unneccesary columns
alldata=alldata.drop(['id','num_private','waterpoint_type_group','source_type','payment_type','extraction_type_group',
            'quantity_group','management_group','quality_group','wpt_name','scheme_name','source_class',
            'date_recorded','recorded_by','subvillage'],axis=1)  
            
alldata.ix[alldata['latitude']>-0.1,'latitude']=None
alldata.ix[alldata['longitude']==0,'longitude']=None
alldata.ix[alldata['funder']=='0','funder']="Other"
alldata.ix[alldata['installer']=='0','installer']="Other"
alldata.ix[alldata['installer']=='-','installer']="Other"
#alldata.ix[alldata['construction_year']==0,'construction_year']=2000
# 2000 is the median of all data excluding 0s

## Data Type
alldata['population']=alldata['population'].astype('float64')           
#alldata['num_private']=alldata['num_private'].astype('float64') 
alldata['gps_height']=alldata['gps_height'].astype('float64') 
alldata['construction_year']=alldata['construction_year'].astype('float64')

## Data TLabel Encoder
le=LabelEncoder()
nullct=np.zeros(alldata.shape[1])
for i in xrange(alldata.shape[1]):
    nullct[i]=sum(pd.isnull(alldata.ix[:,i]))    
    if (nullct[i]>0) & (alldata.columns[i]!='longitude') & (alldata.columns[i]!='latitude'):
        alldata.ix[pd.isnull(alldata.ix[:,i]),i]="Other"   
        ## LabelEncoder
    if alldata.ix[:,i].dtypes=='object':        
        le.fit(alldata.ix[:,i])
        alldata.ix[:,i]=le.transform(alldata.ix[:,i])   

le.fit(outcome['status_group'])
outcome['status_group']=le.transform(outcome['status_group'])

train=alldata.ix[0:trainum-1,:]
test=alldata.ix[trainum:alldata.shape[0],:]
        
## create longitude predict data
#areacol=['latitude','longitude','region','region_code','district_code','lga','ward','gps_height']
#lontrain=alldata.ix[pd.notnull(alldata['latitude']),areacol]
#lontarget=lontrain['latitude']
#lontrain=lontrain.drop(['longitude','latitude'],axis=1)
#lontest=alldata.ix[pd.isnull(alldata['latitude']),areacol]
#lontest=lontest.drop(['longitude','latitude'],axis=1)

## create latitude predict data
#lattrain=alldata.ix[pd.notnull(alldata['longitude']),areacol]
#lattarget=lattrain['longitude']
#lattrain=lattrain.drop(['longitude','latitude'],axis=1)
#lattest=alldata.ix[pd.isnull(alldata['longitude']),areacol]
#lattest=lattest.drop(['longitude','latitude'],axis=1)

train.to_csv('train-c.csv')
test.to_csv('test-c.csv')
outcome.to_csv('target.csv')

#lattrain.to_csv('lat-train-c.csv')
#lattest.to_csv('lat-test-c.csv')
#lattarget.to_csv('lat-target.csv')

#lontrain.to_csv('lon-train-c.csv')
#lontest.to_csv('lon-test-c.csv')
#lontarget.to_csv('lon-target.csv')


etime = float(time.time()-stime)