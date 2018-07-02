# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 11:46:41 2018

@author: lab1x
"""

import pandas as pd
import data_preprocessing as dp
import model_func as mod_func

### Initialize data cleaning classes
sc = dp.sanity_check()
d_agg = dp.data_aggregate()
feat_eng = dp.feature_engineering()

### Readf parameters
with open('parameters.txt') as f:
    for line in f:
        exec(line)

### Read data
data=pd.read_csv('transaction_sample_reduced.csv')

### Data cleaning
# Remove outliers based on low, high percentile, and range
data = sc.run(data, outliers_clean = True, out_columns = out_columns, 
            ills_clean = True, remove_zero = remove_zero, 
            remove_null = remove_null, remove_negative = remove_negative, 
            low = 5, high = 95, range_ = 2)


# Aggregate the data first by assgined level, then filter out the time units with sparse data points.
data = d_agg.run(data, level = 'week', sparse_clean = True, count_ = count_, 
               nunique_ = nunique_, sum_ = sum_, 
               low = 25, high = 75, range_ = 2)

# Clean the measurement list of each category first, convert the OZ into LB ,then calculate unit price.
data = feat_eng.run(data, convert_unit = True, heter_unit_list_1 = heter_unit_list_1, 
            heter_unit_list_2 = heter_unit_list_2, weight_list = weight_list)

# Finalize data
data = sc.finalize(data)

### Initialize train pipeline
train_pipe = mod_func.train_pipleline(data, 'saletotalamount')

### Model training
# Set initial model parameters
train_pipe.set_params(init_params)

# Train model with pipeline
reg, model, importance, score = train_pipe.run(reduce_ = True, grid_ = True, 
                                               param_grid =  {'max_depth':[5, 7, 9], 'n_estimators':[100, 120, 140]}, 
                                               thres = 0.01, scoring = 'neg_mean_absolute_error', verbose = 1)

