# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 22:30:55 2016

@author: meichengshih
"""

import pandas as pd
import numpy as np
import time

train6 = np.loadtxt("blend_train7_50.txt")
test6 = np.loadtxt("blend_pred7_50.txt")
trainl = np.loadtxt("blend_train_log.txt")
testl = np.loadtxt("blend_pred_log.txt")

train8=np.concatenate((train6,trainl),axis=1)
test8=np.concatenate((test6,testl),axis=1)

np.savetxt("blend_train8_50.txt",train8) 
np.savetxt("blend_pred8_50.txt",test8) 