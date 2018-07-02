# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 12:06:17 2018

@author: lab1x
"""
import pandas as pd
from sklearn import ensemble
from sklearn import cross_validation
from sklearn.model_selection import GridSearchCV
import numpy as np

class train_pipleline:
    # Initialization process, prepare the train and target 
    def __init__(self, data, target_column):   
        # Initialize parameters
        self.model = None
        self.importance = None
        self.best_cv_score = None
        
        print("Initializing the gradient boosting tree regresoor")
        self.reg = ensemble.GradientBoostingRegressor(loss='lad', max_depth=7, n_estimators=120, verbose=2)
        
        print("Seperating train and target data set")
        self.target = data[target_column]
        self.train = data.drop([target_column],axis=1)
        self.train_reduce = self.train
    
    # Reinitialize model is neccesary    
    def reinitial_reg(self):
        print("Reinitializing the gradient boosting tree regresoor")
        self.reg = ensemble.GradientBoostingRegressor(loss='lad', max_depth=7, n_estimators=120, verbose=2)
    
    # Train model and obtain importance
    def train_(self, train):
        self.model = self.reg.fit(train, self.target)
        self.importance = pd.DataFrame({'feature':list(train.columns), 'importance':list(self.model.feature_importances_)})  
    
    # Reduce training data features based on feature importances
    def feature_reduce(self, train, thres):
        if self.importance is not None:
            # Determine features to keep based on threshold
            feature_keep=np.array(train.columns)[np.array(self.importance['importance'] >= thres)]
            self.train_reduce = train.loc[:,feature_keep]
        else:
            print("Please train model with full data first to obtain feature importance") 
    
    # Make prediction    
    def predict(self, test):
        if self.reg is not None:
            return self.reg.predict(test)    
        else:
            print("Please train the model before making prediction")
            return None                   
    
    # Do cross validation    
    def cross_val_score(self, train, scoring = 'neg_mean_absolute_error', cv = 5, verbose = 2):
        self.best_cv_score = cross_validation.cross_val_score(estimator = self.reg , train= train, target = self.target, 
                                                 scoring = scoring, cv = cv, verbose = verbose).mean()
        
    # Do grid search
    def grid_search(self, train, param_grid, scoring, reduce_, verbose):        
        grid = GridSearchCV(self.reg, cv = 5, n_jobs = 1, param_grid = param_grid, scoring= scoring, verbose = verbose)
        result_ = grid.fit(train, self.target)
        
        self.best_cv_score = result_.best_score_ 
        self.reg = result_.best_estimator_
    
    # Get trained model
    def get_model(self):
        if self.model is not None:
            return self.model
        else:
            print("Model empty")
            return None
        
    # Get feature importance    
    def get_importance(self):
        if self.importance is not None:
            return self.importance
        else:
            print("Importance empty")
            return None
        
    # Get train or train_reduce data    
    def get_train(self, reduce_ = False):
        if reduce_:
            return self.train_reduce
        elif reduce_ == False:
            return self.train
        else:
            print("Train set empty")
            return None
        
    def get_score(self):
        if self.best_cv_score is not None:
            return self.best_cv_score
        else:
            print("CV score empty")
            return None
        
    def get_target(self):
        if self.target is not None:
            return self.target
        else:
            print("Target feature set empty")
            return None
    
    # Set parameters of the initial regressor 
    def set_params(self, params):
        self.reg.set_params(**params)                
        
    # Main data pipeline     
    def run(self, reduce_ = True, grid_ = True, param_grid =  {'max_depth':[5, 7, 9], 'n_estimators':[100, 120, 140]}, 
            thres = 0.01, scoring = 'neg_mean_absolute_error', verbose = 2):
        # Set training data
        train = self.train
        
        # Train with important fearures only?
        if reduce_:
            self.train_(train)
            self.feature_reduce(train, thres =thres)
            train = self.train_reduce    
        
        # Do grid search?
        if (grid_):
            self.grid_search(train, param_grid = param_grid, scoring = scoring, reduce_ = reduce_, verbose = verbose)
        
        else:
            # Use cross validation to obtain cv score
            self.cross_val_score(train, scoring = 'neg_mean_absolute_error', cv = 5, verbose = verbose)
            # Train model to get model
            self.train_(train)
                        
        return self.reg, self.model, self.importance, -self.best_cv_score
            
            
        
        
