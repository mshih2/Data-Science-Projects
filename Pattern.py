
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 09:18:16 2017

@author: lab1x
"""

import sys

def printf(format, *args):
    sys.stdout.write(format % args)

class Node(object):
    def __init__(self, status):
        self.status = status
        self.count= 1
        self.dep=0
        self.tm_median=0
        self.tm_mean=0
        self.tm_std=0
        self.time =list()
        self.child = dict()

    def add_child(self, node, tm):
        self.child[node.status]=node
        self.count += 1
        self.time.append(tm)

    def add_child_ct(self, item, tm):
        self.count += 1 
        self.time.append(tm)
        
    def get_child(self, item):
        return self.child[item]


class pattern_tree(object):    
    def __init__(self):
        self.root=Node('-')
        self.patterns = []
        self.patterns_val = []
        self.rep=True
    
    def train(self, rawdata, rep=True, ind='median'):
        self.rep=rep
        def train_row(status):            
            items = status[0].split("|")
            items=list(map(str.strip, items))
            items=list(filter(None, items))
            cur=self.root
            pre_status=""
            temp_set=set()
            for item in items:
                if ((item!=pre_status) and (item not in temp_set)):
                    if not self.rep:
                        temp_set.add(item)
                        
                    if item not in cur.child:
                        cur.add_child(Node(item), status[1])
                        cur=cur.get_child(item)

                    else:
                        cur.add_child_ct(item, status[1])
                        cur=cur.get_child(item)
                    
                    if item==items[-1].strip():
                        cur.time.append(status[1])
                    
                    if ((cur.status==['AS']) & (cur.dep>1)):
                        print ('AS not in first layer!')

                pre_status=item

        rawdata=rawdata.apply(train_row,axis=1)
                    
        self.calculate_mean_and_var()
        self.check_ct_values()
        self.find_patterns(self.root,ind)
        
    def calculate_mean_and_var(self):
        self.mean_var_recur(self.root)
               
    def mean_var_recur(self, cur):
        import numpy as np
        cur.tm_median=np.median(cur.time)
        cur.tm_mean=np.mean(cur.time)
        cur.tm_std=np.std(cur.time)
        if not any(cur.child):
            return [cur.status]
        else:
            for k in cur.child:
                self.mean_var_recur(cur.child[k])
                    
    def find_patterns (self, node, ind):
        self.patterns=self.patterns_recur(self.root, ind)
    
    def patterns_recur(self, node, ind):
        if node is None:
            return []

        if ((node.count<0)|(not any(node.child))):
            if ind=='median':    
                self.patterns_val.append(node.tm_median)
            else:
                self.patterns_val.append(node.tm_mean)
            return [node.status]
                
        
        full_sub=[]
        for k in node.child:
            full_sub+=self.patterns_recur(node.child[k], ind)
        
        patterns=[]
  
        for leaf in full_sub:
            patterns.append(node.status+'->'+leaf)
  
        return patterns
    
    def get_end_node(self, pattern):
        items=pattern.split("|")
        items=list(map(str.strip, items))
        items=list(filter(None, items))
        pre_status=""
        cur=self.root
        temp_set=set()
        rep=True
        for item in items:
            if ((item!=pre_status) and (item!="") and (item not in temp_set)):
                if rep:
                    temp_set.add(item)
                if ((not any(cur.child)) | (item not in cur.child)):
                    return cur
                else:
                    cur=cur.get_child(item)

            pre_status=item
        return cur
        
    def predict(self, rawdata, ind='median',rep=True):
        import numpy as np
        prediction=list()
        
        def get_mean(pattern): 
            return self.get_end_node(pattern).tm_mean
        
        def get_median(pattern):
            return self.get_end_node(pattern).tm_median
        
        if ind not in ['median','mean']:
            print ("index should be median or mean")
            return
        if ind=='median':
            prediction=rawdata.apply(get_median)
        else:
            prediction=rawdata.apply(get_mean)
        return np.array(prediction)
        
    def ct_value_recur(self, cur):
        if not cur.time:
            print ("historical time list is empty!")
        if not any(cur.child):
            return
        else:
            for k in cur.child:
                self.ct_value_recur(cur.get_child(k))
                
    def check_ct_values(self):
        self.ct_value_recur(self.root)
    
            

    
              
    