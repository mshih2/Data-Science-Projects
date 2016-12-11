# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:54:16 2016

@author: Mei-Cheng Shih
"""
import time
### need to divide delay files into seperate csv files
stime = time.time()
cases= range(0,27)

n=10000


def caseinput(case,departure,traffic,rawdata):
    traffic_m=case%3
    rawdata.ix[traffic.ix[:,case]=='T',1]=departure.ix[traffic.ix[:,case]=='T',traffic_m]
    rawdata.ix[traffic.ix[:,case]=='F',1]=-5000
    rawdata.ix[traffic.ix[:,case]=='T',2]=rawdata.ix[traffic.ix[:,case]=='T',1]+242/rawdata.ix[traffic.ix[:,case]=='T',6]
    rawdata.ix[traffic.ix[:,case]=='F',2]=-5000    
    rawdata.ix[:,13]=traffic.ix[:,case]
    rawdata=rawdata.values.tolist()
        
    return rawdata
    

class CalSchedule(object):
    def __init__(self,case,trainnum,tolerance):
       import numpy as np
       self.statlist=np.zeros((trainnum,5))
       self.statlist_n=np.zeros((trainnum,5))
       self.case=case
       self.tol=tolerance
       self.gap=5
     
    def stpoint(self, spd, strpoint, dep):
        if dep>0:
            if strpoint==0:
                return (24-float(dep))*float(spd)
            else:
                return 242-(24-float(dep))*float(spd)
        elif dep<0:
            if strpoint==0:
                return abs(float(dep))*float(spd)
            else:
                return 242-abs(float(dep))*float(spd)

    def depover(self,row):
        new_train=list(row)
        new_train[1]=0
        new_train[2]=row[2]-24
        new_train[4]=self.stpoint(row[6],row[4],row[1])
        new_train[5]=0
        new_train[7]='Y'
        new_train[0]=row[0]+'-n'
        return (new_train)

    def depless(self,row):
        new_train=list(row)
        new_train[1]=24+row[1]
        new_train[2]=24
        new_train[4]=row[4]
        new_train[5]=0
        new_train[7]='Y'
        new_train[0]=row[0]+'-n'
        return (new_train) 

    def random_schedule(self,rawdata):
        import numpy as np       
        numcol=[1,2,4,5,6,8,9,10,11]
        for row in rawdata:
            for j in numcol:
                row[j]=float(row[j])
        self.tname=np.matrix(rawdata)[:,12]
        self.rdata=[x[:] for x in rawdata]
        
        # Write Departure and Arrival time to the read format         
        
        
        for row in self.rdata:
            if row[7]=='N':
                row[1]=row[1]+row[5]*random.uniform(-1, 1)
                #row[1]=row[1]
                row[2]=row[1]+242/float(row[6])  
                row[4]=row[4]
            # create overnight train list
                if row[1]>24 and row[2]>24:
                    row[1]=row[1]-24
                    row[2]=row[2]-24
                elif row[1]<24 and row[2]>24:
                    self.rdata.append(self.depover(row))
                    row[2]=24
                # create previous night train list
                elif row[1]<0 and row[2]<0:
                    row[1]=24+row[1]
                    row[2]=24+row[2]
                elif row[1]<0 and row[2]>0:
                    self.rdata.append(self.depless(row))
                    row[4]=self.stpoint(row[6],row[4],row[1])
                    row[1]=0

    def ab_cal(self):
        for row in self.rdata:
            if row[3]=='E':
                row[9]=  row[6]
                row[10]= row[4]-row[9]*row[1]
            else:
                row[9]=  -row[6]
                row[10]= row[4]-row[9]*row[1]

    def index_cal(self,i):
        import numpy as np
        if i>0:
            self.statlist_old=self.statlist/(i+1)
            
        for obj in self.rdata:   
            for tar in self.rdata:
                if all([obj[0]!=tar[0],obj[9]!=tar[9],tar[13]=='T']):
                    conflict_t=(tar[10]-obj[10])/float(obj[9]-tar[9])
                    conflict_d=obj[9]*conflict_t+obj[10]
                    if all([conflict_t>=0, conflict_t<=24, conflict_d>=0, conflict_d<=242]):
                # total conflict
                        self.statlist[np.where(obj[12]==self.tname)[0],0]+=1
                # inferior meet (stop meet)
                        if (obj[8]>tar[8] and obj[3]!=tar[3]):
                            self.statlist[np.where(obj[12]==self.tname)[0],1]+=1
                # equal meet (stop meet)               
                        if (obj[8]==tar[8] and obj[3]!=tar[3]):
                            self.statlist[np.where(obj[12]==self.tname)[0],1]+=0.5 
                # inferior pass                
                        if (obj[8]>tar[8] and obj[3]==tar[3]):
                            self.statlist[np.where(obj[12]==self.tname)[0],2]+=1
        if i>0:
            self.statlist_n=self.statlist/(i+1)
            # check convegence
            self.gap=max((self.statlist_n-self.statlist_old)[(self.statlist_n-self.statlist_old)!=0])
            self.statlist_n[:,3]=self.case


if __name__ == "__main__":
    import pandas as pd
    import random
    delay=pd.read_csv('delay.csv')
    departure=pd.read_csv('27Scenarios-Departure.csv', header=None)
    traffic=pd.read_csv('27Scenarios-Traffic.csv', header=None)
    rawdata=pd.read_csv('base_schedule.csv', header=None, index_col=None)
    
    trainnum=36
    ct=False
    for case in cases:
        print "Processing Schedule "+str(case) 

        rawdata2=caseinput(case,departure,traffic,rawdata)

        k=CalSchedule(str(case),trainnum,1e-3)
        random.seed(900)
        for i in xrange(n):
            k.random_schedule(rawdata2)
            k.ab_cal()
            k.index_cal(i)
        
            if (i>0) & (k.gap<k.tol):
                print ('Reached termination criteria, stopped at iteration '+str(i)+' with gap '+str(k.gap))
                break
                print (i)
        
        if ct==False:
            z=pd.DataFrame(k.statlist_n)
            z.ix[:,4]=k.tname
            ct=True
        else:
            znew=pd.DataFrame(k.statlist_n)
            znew.ix[:,4]=k.tname
            z=pd.concat([z,znew],axis=0)
        
    z.columns=['TC','ATP','IP','Case','Train']
    output=pd.merge(z,delay, left_on=['Case','Train'], right_on=['Case','Train'])
    output=output.drop(['Case','Train'],axis=1)
    output.to_csv('output.csv')
    
    
       
    
etime = float(time.time()-stime)       
