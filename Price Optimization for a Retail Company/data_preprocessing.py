# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 11:46:41 2018

@author: lab1x
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing

## Clean the outliers and data points with illogical feature values
class sanity_check:
    ## Remove outliers based on low, high percentile, and range
    def remove_outliers(self, *argv):
        a=np.array(argv[0])
        upper_ = np.percentile(a, argv[2])
        lower_ = np.percentile(a, argv[1])
        IQR = (upper_ - lower_) * argv[3]
        quartileSet = (lower_ - IQR, upper_ + IQR)
        ind = ((a >= quartileSet[0]) & (a <= quartileSet[1]))
        return ind 
    
    ## Remove outliers by columns
    def remove_column_outliers(self, data, *argv): # data, out_columns, low=25, high=75, range_=2
        for column in argv[0]: 
            orig_len = len(data)
            ind = self.remove_outliers(data[column], argv[1], argv[2], argv[3])
            data = data.loc[ind,:] 
            print ('{} outliers on \'{}\' column removed, using low percentile {}, high percentile {}, and range {}'
                   .format(orig_len - len(data), column, argv[1], argv[2], argv[3]))
        return data

    ## Delete data with zero, null and negative values in different columns based on assigned rules
    def remove_ill(self, *argv): #data, remove_zero, remove_null, remove_negative
        print ('Removing illogical values')
        # remove data points with assigned column equal to zero
        print ('{} data points with 0 values from \'{}\' column(s) removed'.format((argv[0][argv[1]] == 0).sum().values[0], argv[1]))
        remove_zero_ind = (argv[0][argv[1]] != 0).all(axis = 1)
        # remove data points with assigned column equal to null
        print ('{} data points with null values from \'{}\' column(s) removed'.format(argv[0][argv[2]].isnull().sum().values[0], argv[2]))
        remove_null_ind = (argv[0][argv[2]].isnull() == False).all(axis = 1)
        # remove data points with assigned column equal to negative
        print ('{} data points with negative values from \'{}\' column(s) removed'.format((argv[0][argv[3]] < 0).sum().values[0], argv[3]))
        remove_negative_ind = (argv[0][argv[3]] >= 0).all(axis = 1)
        return argv[0].loc[remove_zero_ind & remove_null_ind & remove_negative_ind,:]
    
    ## A run function combine both executions
    def run(self, data, outliers_clean=True, out_columns=[], ills_clean=True, 
            remove_zero = [], remove_null = [], remove_negative = [], 
            low = 25, high = 75, range_ = 2): 
        # Detect outliers or not
        if ills_clean==True:
            data = self.remove_ill(data, remove_zero, remove_null, remove_negative)      
        # Detect illogical values or not
        if outliers_clean==True:
            data = self.remove_column_outliers(data, out_columns, low, high, range_)
            
        return data
    
    ## Finalize data and drop uneccesary columns
    def finalize(self, data):
        # Convert categorical features into integer categories
        print ("Finalizing data for training")
        for column in data.columns:
            if data[column].dtype=='O':
                enc = preprocessing.LabelEncoder()
                data[column] = enc.fit_transform(data[column])
        
        data = data.drop(['id','date','time_unit'], axis=1)
        
        return data
    
## Aggregate the data first by assgined level, then filter out the time units with sparse data points.
## The assigned level depends on the concern of the prediction model, if predicting weekly sales,
## set level to 'week', if daily, use 'day'
class data_aggregate:   
    # Generate agg time unit
    def gen_time_unit(self, data, level):
        if level not in ['week','day']:
            print ('Warning: the input level is not regonized, so time unit aggregation will not be used')
            
        print ('Generating time unit based on {}'.format(level))
        data['date'] = pd.to_datetime(data['date'], format='%m/%d/%Y')
        if level == 'week':
            data['time_unit'] = np.floor((data['date'] - min(data['date'])).dt.days / 7) + 1 
        elif level == 'day':
            data['time_unit'] = (data['date'] - min(data['date'])).dt.days 
        else:
            data['time_unit'] = data.index.values
            
        return data    
    
    # Delete time unit with small data points 
    def clean_sparse_time_unit(self, data, *argv):  # (count_, nunique_, sum_, low, high, range_)
        if 'time_unit' not in data.columns:
            print ("Time_unit feature must be generated before cleaninig sparse time unit")
            return None
        # Import sanity_check to use outlier detection function
        sc = sanity_check()
        # Name of three sections
        section_name=['count', 'unique number', 'sum value']
        # clean time units without enough data points
        ct = 0
        for section in [argv[0],argv[1],argv[2]]:
            ct += 1
            # Loop over categories
            for column in section:
                if column:
                    
                    # Count
                    if ct == 1:
                        std_val= data.groupby([column])[column].count()
                    # Unique count
                    elif ct== 2:
                        std_val= data.groupby([column])[column].nunique()
                    # Sum value
                    else: 
                        std_val= data.groupby([column])[column].sum()
                        
                    # Location of outliers
                    loc_ = sc.remove_outliers(std_val, argv[3], argv[4], argv[5])
                    loc_ = np.where(loc_)[0].tolist()
                    print('{} data points with sparse time unit based on the \'{}\' column in {} category'
                          .format(sum(data['time_unit'].isin(loc_)==False), column, section_name[ct-1]))
                    data=data.loc[data['time_unit'].isin(loc_),:] 
                    
        return data 
      
    def run(self, data, level = 'week', sparse_clean = True, count_ = [], nunique_ = [], sum_ = [], 
            low = 25, high = 75, range_ = 2):
        
        data=self.gen_time_unit(data, level)
        # Clean sparse data or not
        if sparse_clean==True:
            data=self.clean_sparse_time_unit(data, count_, nunique_, sum_, low, high, range_)
            
        return data
            
## Clean the measurement list of each category first, convert the OZ into LB ,then calculate unit price.
## If the measurement lists are not cleaned, then the output unit price will be the original price      
class feature_engineering:   
    def __init__(self):
        # Denoting if the measurements are cleaned and the production size is standardized
        self.unit_clean = False
        self.unit_std = False
        
    # Find uniuqe measurement list for each product category
    def find_unit_list(self, data):
        unit_list=data.groupby(['category'])['productmeasure'].unique().apply(set)
        
        return unit_list
    
    # Find the unique list of unique unit list for all categories
    def find_unit_unique_list(self, data):
         
        unit_list=data.groupby(['category'])['productmeasure'].unique().apply(set)
        unique_unit_list = [list(x) for x in set([tuple(set(x)) for x in unit_list])]
        
        return unique_unit_list
    
    # Delete the data points with minority measurement, or multiple measurement types, 
    # in order to make the unit conversion process reasonable    
    def delete_minor_unit_group(self, data, heter_unit_list_1, heter_unit_list_2, unit_list):
        for ind, unit in enumerate(unit_list):
            # Delete data points with 'count' measurement in the categories with 
            # both 'count' and weight-related (OZ, LB, ...) measurements
            if  list(unit) in heter_unit_list_1:
                data = data.loc[((data['category'] == unit_list.index[ind]) & (data['productmeasure'] == 'CT')) == False,:]
            # Delete data points in cateogories with multiple measurement type or unknown measurement type
            elif list(unit) in heter_unit_list_2:
                data = data.loc[(data['category'] != unit_list.index[ind]),:]
            
        return data
    
    # Convert weight to same unit
    def weight_converter(self, data, unit_list, weight_list):
        for ind, unit in enumerate(unit_list):
            if  list(unit) in weight_list:
                data.loc[((data['category'] == unit_list.index[ind]) & (data['productmeasure'] == 'LB')),'productsize'] *= 1 / 0.0625
                data.loc[((data['category'] == unit_list.index[ind]) & (data['productmeasure'] == 'LB')),'productmeasure'] = 'OZ'
        
        return data
    
    # Calculate unit price
    def unit_price(self, data):
        if ((self.unit_clean == True) & (self.unit_std == True)):
            print ("Generating unit price based on standardized units")
        else:
            print ("Generating unit price based on non-standardized units")
            
        
        # Generate training target
        data['saletotalamount'] = data['purchasequantity'] * data['productsize']
        # Calculate unit price = purchaseamount / (purchasequanitity*productsize)
        data['unitprice'] = data['purchaseamount'] / (data['saletotalamount']) 
        # Drop these two features since they were used for engineering
        data = data.drop(['purchasequantity', 'productsize', 'purchaseamount'],axis=1)
    
        return data
    
    def run(self, data, convert_unit = True, 
            heter_unit_list_1 = [['RL', 'CT'],['YD', 'CT'],['OZ', 'CT'],['LB', 'CT'],['LB', 'OZ', 'CT']], 
            heter_unit_list_2 = [['YD', 'FT', 'LB', 'OZ', 'CT'],['1', 'CT']], weight_list = [['LB', 'OZ']]):
       
       # The process need to convert data
       if convert_unit == True:
           unit_list = self.find_unit_list(data) 
           data = self.delete_minor_unit_group(data, heter_unit_list_1, heter_unit_list_2, unit_list)
           self.unit_clean = True
           data = self. weight_converter(data, unit_list, weight_list)
           self.unit_std = True
           
       data = self.unit_price(data)
       
       return data
    


