# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 11:57:04 2018

@author: meichengshih
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def removeOutliers(x, low, high):
    a = np.array(x)
    upper_quartile = np.percentile(a, high)
    lower_quartile = np.percentile(a, low)
    IQR = (upper_quartile - lower_quartile) * 2
    quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
    resultList = []
    for i,y in enumerate(a.tolist()):
        if y >= quartileSet[0] and y <= quartileSet[1]:
            resultList.append(i)
    return set(resultList)   

# Read data
data=pd.read_csv('transactions_sampled.csv')

## Step 1, delete data with negative and null values
data=data.loc[((data['category']!=0)&(data['productmeasure'].isnull()!=True)&(data['purchaseamount']>0)&(data['purchasequantity']>0)&(data['productsize']>0)),:]

## Step 2, delete bulk purchase data, by using interquantile rule
## brand count was added to consider the interaction between prices of brands

data=data.iloc[list(removeOutliers(data['purchaseamount'], 10,90)),:]

# calculate day index
data['week']=np.floor((pd.to_datetime(data['date'])-min(pd.to_datetime(data['date']))).dt.days/7)+1


# find number of data point for each day
week_ct=data.groupby(['week'])['week'].count()

# find quantityt for each day, and the average amount of each purchase
week_quan_ct=data.groupby(['week'])['purchaseamount'].sum()

# find brand number
week_brand_ct=data.groupby(['week'])['brand'].nunique()

# find the days to keep based on interquartile rule, since the brand diversity and sale number are too low for some of the days
week_keep= set.intersection(removeOutliers(week_brand_ct,25,75), removeOutliers(week_ct,25,75), removeOutliers(week_quan_ct,25,75))
data=data.loc[data['week'].isin(np.array(week_ct.index)[list(week_keep)]),:]

## Step 3, convert product size of each category into one standardized unit 
# find uniuqe measure list for each product
unit_list=data.groupby(['category'])['productmeasure'].unique().apply(set)

# used to check the count of each combination of units in categories, it seems the counts of the categoris 
# with multiple units are all small
unique_unit_list = [list(x) for x in set([tuple(set(x)) for x in unit_list])]
cnt_unit={}
for unit in unique_unit_list:
    cnt_unit['_'.join(unit)]=sum([1 for i in unit_list if set(i)==set(unit)])
    
# after checking the unit manually, it is found that for:
for ind, unit in enumerate(unit_list):    
    if  list(unit) in [['RL', 'CT'],['YD', 'CT'],['OZ', 'CT'],['LB', 'CT'],['LB', 'OZ', 'CT']]:
        data=data.loc[((data['category']==unit_list.index[ind]) & (data['productmeasure']=='CT'))==False,:]
    elif list(unit) in [['YD', 'FT', 'LB', 'OZ', 'CT'],['1', 'CT']]:
        data=data.loc[(data['category']!=unit_list.index[ind]),:]

# re do the list
unit_list=data.groupby(['category'])['productmeasure'].unique().apply(set)  
unique_unit_list = [list(x) for x in set([tuple(set(x)) for x in unit_list])] 

# convert product size from LB into OZ for categories with OZ and LB 
for ind, unit in enumerate(unit_list):
    if  list(unit) in [['LB', 'OZ']]:
        data.loc[((data['category']==unit_list.index[ind]) & (data['productmeasure']=='LB')),'productsize']*=1/0.0625
        data.loc[((data['category']==unit_list.index[ind]) & (data['productmeasure']=='LB')),'productmeasure']='OZ'
        
## Step 4, calculate unit price 
data['saletotalamount']=data['purchasequantity']*data['productsize']
data['unitprice']=data['purchaseamount']/(data['saletotalamount'])                    

## Step 5, try to visdualize total saled amount versus of one category by week
## Use log linear function to fit
tmp=data.loc[((data['productmeasure']=='OZ')&(data['category']==907)),:]
tmp=tmp.iloc[list(removeOutliers(tmp['unitprice'],25,75)),:]
k=tmp.groupby(['chain','category','week','brand','company'])['saletotalamount'].sum()
k2=tmp.groupby(['chain','category','week','brand','company'])['unitprice'].mean()
k=pd.concat([k, k2], axis=1)
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(k['saletotalamount']),k['unitprice'])
line = slope*np.log(k['saletotalamount'])+intercept
              
plt.plot(k['saletotalamount'], k['unitprice'],'o', k['saletotalamount'], line,'o')

## The output fits understanding (higher the price, less the quantity),
## so it means the general trend of quantity and unit price is reasonable

## Step 6, convert original data into week-based data
# Time related
data['date']=pd.to_datetime(data['date'])
data['monthinyear']=data['date'].dt.month
data['weekinyear']=data['date'].dt.week
data['quarter']=data['date'].dt.quarter
data['month']=data['date'].dt.month+12*(data['date'].dt.year-min(data['date'].dt.year))

data_d=data.groupby(['chain','category','monthinyear','weekinyear','quarter','brand','company','productmeasure','month','week'])['saletotalamount'].sum()
data_d2=data.groupby(['chain','category','monthinyear','weekinyear','quarter','brand','company','productmeasure','month','week'])['unitprice'].mean()
data_d=pd.concat([data_d, data_d2], axis=1)
data_d=data_d.reset_index()

## Step 7, lets add more features
# Relative prices in other time stamp
# find rate of this unitprice to the median unitprice of this week
k=data_d.groupby(['chain','category','week'])['unitprice'].median().reset_index()
k=k.rename(columns={'unitprice':'aveunitprice'})
data_d=pd.merge(data_d, k, on=['chain','category','week'], how='left')
data_d['aveunitprice']=data_d['aveunitprice']/data_d['unitprice']
print (len(data_d))

# find rate of today to median of previous week
k['week']-=1
k=k.rename(columns={'aveunitprice':'aveunitpricelast'})
data_d=pd.merge(data_d, k, on=['chain','category','week'], how='left')
data_d['aveunitpricelast']=data_d['aveunitpricelast']/data_d['unitprice']
data_d['aveunitpricelast']=data_d['aveunitpricelast'].fillna(-1)
print (len(data_d))

# find rate of today to median of 2 previous week
k['week']-=1
k=k.rename(columns={'aveunitpricelast':'aveunitpricelast2'})
data_d=pd.merge(data_d, k, on=['chain','category','week'], how='left')
data_d['aveunitpricelast2']=data_d['aveunitpricelast2']/data_d['unitprice']
data_d['aveunitpricelast2']=data_d['aveunitpricelast2'].fillna(-1)
print (len(data_d))

# find rate of today to median of this month
k=data_d.groupby(['chain','category','month'])['unitprice'].median().reset_index()
k=k.rename(columns={'unitprice':'aveunitpricemonth'})
data_d=pd.merge(data_d, k, on=['chain','category','month'], how='left')
data_d['aveunitpricemonth']=data_d['aveunitpricemonth']/data_d['unitprice']
data_d['aveunitpricemonth']=data_d['aveunitpricemonth'].fillna(-1)
print (len(data_d))

# find rate of today to median of last month
k['month']-=1
k=k.rename(columns={'aveunitpricemonth':'aveunitpricemonthlast'})
data_d=pd.merge(data_d, k, on=['chain','category','month'], how='left')
data_d['aveunitpricemonthlast']=data_d['aveunitpricemonthlast']/data_d['unitprice']
data_d['aveunitpricemonthlast']=data_d['aveunitpricemonthlast'].fillna(-1)
print (len(data_d))

# find rate of today to median of the second month before
k['month']-=1
k=k.rename(columns={'aveunitpricemonthlast':'aveunitpricemonthlast2'})
data_d=pd.merge(data_d, k, on=['chain','category','month'], how='left')
data_d['aveunitpricemonthlast2']=data_d['aveunitpricemonthlast2']/data_d['unitprice']
data_d['aveunitpricemonthlast2']=data_d['aveunitpricemonthlast2'].fillna(-1)
print (len(data_d))

# drop functional features
data_d=data_d.drop(['month','week'],axis=1)

# write to csv
data_d.to_csv('transaction_clean_week.csv',index=False)
