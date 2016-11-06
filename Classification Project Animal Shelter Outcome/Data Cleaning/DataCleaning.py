# -*- coding: utf-8 -*-
"""
Created on Sun May 08 17:55:06 2016

@author: meichengshih
"""

#### Adult dog (year 1)?
#### Hair Length?
#### dog size

import pandas as pd
import time
import numpy as np
import holidays
from sklearn.preprocessing import LabelEncoder

small=0

stime = time.time()

## read input
#trainname='/Users/meichengshih/Dropbox/Kaggle/Shelter Animal Outcomes/train.csv'
trainname="/Users/meichengshih/Dropbox/Kaggle/Shelter Animal Outcomes/train.csv"
testname="/Users/meichengshih/Dropbox/Kaggle/Shelter Animal Outcomes/test.csv"
colorname="/Users/meichengshih/Dropbox/Kaggle/Shelter Animal Outcomes/color.csv"
weightname="/Users/meichengshih/Dropbox/Kaggle/Shelter Animal Outcomes/breed_weight.csv"
weight=pd.read_csv(weightname, index_col=False)
data=pd.read_csv(trainname, index_col=False)
data=data.drop(data.columns[[0,4]], axis=1) 
datatest=pd.read_csv(testname, index_col=False)
datatest=datatest.drop(datatest.columns[[0]], axis=1) 
colorlist=pd.read_csv(colorname, index_col=False)

### Name ###
data.ix[pd.isnull(data["Name"])==False,"Name"]=1
datatest.ix[pd.isnull(datatest["Name"])==False,"Name"]=1
data.ix[pd.isnull(data["Name"])==True,"Name"]=0
datatest.ix[pd.isnull(datatest["Name"])==True,"Name"]=0


#name=pd.concat([data["Name"],datatest["Name"]],axis=0)
#namefreq=name.value_counts()/(name.value_counts()[1]+10)
#namefreq[0]=1
#for i in xrange(len(namefreq)):
#    data.ix[data["Name"]==np.array(namefreq.index)[i],"Name"]=namefreq[i]
#    datatest.ix[datatest["Name"]==np.array(namefreq.index)[i],"Name"]=namefreq[i]

### Date ###
dttime=pd.DataFrame(columns=["Year","Month","Day","Hour","DayofWeek","WeekofYear","Holiday"])
dttimetest=pd.DataFrame(columns=["Year","Month","Day","Hour","DayofWeek","WeekofYear","Holiday"])
DateTime=pd.DatetimeIndex(data["DateTime"])
DateTimetest=pd.DatetimeIndex(datatest["DateTime"])

dttime["Year"]=DateTime.year
dttime["Month"]=DateTime.month
dttime["Day"]=DateTime.day
dttime["Hour"]=DateTime.hour+DateTime.minute/float(60)
dttime["DayofWeek"]=DateTime.dayofweek
dttime["WeekofYear"]=DateTime.weekofyear

dttimetest["Year"]=DateTimetest.year
dttimetest["Month"]=DateTimetest.month
dttimetest["Day"]=DateTimetest.day
dttimetest["Hour"]=DateTimetest.hour+DateTimetest.minute/float(60)
dttimetest["DayofWeek"]=DateTimetest.dayofweek
dttimetest["WeekofYear"]=DateTimetest.weekofyear


# Holidays
dttime.ix[:,"Holiday"]=0
for i in range(len(data)):
    if data.ix[i,"DateTime"] in holidays.US():
       dttime.ix[i,"Holiday"]=1
    
    if (dttime.ix[i,"DayofWeek"] ==6) | (dttime.ix[i,"DayofWeek"] ==7):
        dttime.ix[i,"Holiday"]=1

dttimetest.ix[:,"Holiday"]=0
for i in range(len(datatest)):
    if datatest.ix[i,"DateTime"] in holidays.US():
       dttimetest.ix[i,"Holiday"]=1
    
    if (dttimetest.ix[i,"DayofWeek"] ==6) | (dttimetest.ix[i,"DayofWeek"] ==7):
        dttimetest.ix[i,"Holiday"]=1

# Drop columns
data=data.drop("DateTime", axis=1)
datatest=datatest.drop("DateTime", axis=1)

## Counting Number of Data Points of each Year-Month
#dttime.groupby(['Year', 'Month']).size()

### Sex ###
sex=data.ix[:,3].str.split(" ",expand=True)
sex.columns=["Fertility","Sex"]
sex.ix[sex["Fertility"]=="Unknown", "Sex"]="Unknown"
data=data.drop("SexuponOutcome", axis=1)

sextest=datatest.ix[:,2].str.split(" ",expand=True)
sextest.columns=["Fertility","Sex"]
sextest.ix[sextest["Fertility"]=="Unknown", "Sex"]="Unknown"
datatest=datatest.drop("SexuponOutcome", axis=1)

### Age ##
age=data.ix[:,3].str.split(" ",expand=True)
age.ix[:,0]=pd.to_numeric(age.ix[:,0])
age.columns=["Age","Unit"]
# months and weeks and days
age.ix[(age["Unit"]=="year"),"Age"]=age["Age"]*float(365)
age.ix[(age["Unit"]=="years"),"Age"]=age["Age"]*float(365)
age.ix[(age["Unit"]=="month"),"Age"]=age["Age"]*float(30)
age.ix[(age["Unit"]=="months"),"Age"]=age["Age"]*float(30)
age.ix[(age["Unit"]=="week"),"Age"]=age["Age"]*float(7)
age.ix[(age["Unit"]=="weeks"),"Age"]=age["Age"]*float(7)
age.ix[(age["Unit"]=="day"),"Age"]=age["Age"]
age.ix[(age["Unit"]=="days"),"Age"]=age["Age"]
age.ix[pd.isnull(age["Age"]),"Age"]=np.mean(age["Age"])
age=age.drop(age.columns[[1]], axis=1)
data=data.drop("AgeuponOutcome", axis=1)

agetest=datatest.ix[:,2].str.split(" ",expand=True)
agetest.ix[:,0]=pd.to_numeric(agetest.ix[:,0])
agetest.columns=["Age","Unit"]
# months and weeks and days
agetest.ix[(agetest["Unit"]=="year"),"Age"]=agetest["Age"]*float(365)
agetest.ix[(agetest["Unit"]=="years"),"Age"]=agetest["Age"]*float(365)
agetest.ix[(agetest["Unit"]=="month"),"Age"]=agetest["Age"]*float(30)
agetest.ix[(agetest["Unit"]=="months"),"Age"]=agetest["Age"]*float(30)
agetest.ix[(agetest["Unit"]=="week"),"Age"]=agetest["Age"]*float(7)
agetest.ix[(agetest["Unit"]=="weeks"),"Age"]=agetest["Age"]*float(7)
agetest.ix[(agetest["Unit"]=="day"),"Age"]=agetest["Age"]
agetest.ix[(agetest["Unit"]=="days"),"Age"]=agetest["Age"]
agetest.ix[pd.isnull(agetest["Age"]),"Age"]=np.mean(agetest["Age"])
agetest=agetest.drop(agetest.columns[[1]], axis=1)
datatest=datatest.drop("AgeuponOutcome", axis=1)

### Breed ###
# Replace Weird Black Tan Hound Name
# Replace abbreviations and unify simialr terms
data["Breed"]=data["Breed"].str.replace("Black/Tan Hound","Black Tan Hound")
datatest["Breed"]=datatest["Breed"].str.replace("Black/Tan Hound","Black Tan Hound") 
data["Breed"]=data["Breed"].str.replace("Chesa Bay Retr","Chesa Bay Retriever")
datatest["Breed"]=datatest["Breed"].str.replace("Chesa Bay Retr","Chesa Bay Retriever") 
data["Breed"]=data["Breed"].str.replace("Retr ","Retriever ")
datatest["Breed"]=datatest["Breed"].str.replace("Retr ","Retriever ") 
data["Breed"]=data["Breed"].str.replace("Terr ","Terrier ")
datatest["Breed"]=datatest["Breed"].str.replace("Terr ","Terrier ") 
data["Breed"]=data["Breed"].str.replace("Patterdale Terr","Patterdale Terrier")
datatest["Breed"]=datatest["Breed"].str.replace("Patterdale Terr","Patterdale Terrier")
data["Breed"]=data["Breed"].str.replace("Patterdale Terrierier","Patterdale Terrier")
datatest["Breed"]=datatest["Breed"].str.replace("Patterdale Terrierier","Patterdale Terrier")    
data["Breed"]=data["Breed"].str.replace("Sh ","Shorthair ")
datatest["Breed"]=datatest["Breed"].str.replace("Sh ","Shorthair ")  
data["Breed"]=data["Breed"].str.replace("Eng ","English ")
datatest["Breed"]=datatest["Breed"].str.replace("Eng ","English ") 
data["Breed"]=data["Breed"].str.replace("Dachshund Stan","Dachshund")
datatest["Breed"]=datatest["Breed"].str.replace("Dachshund Stan","Dachshund")
data["Breed"]=data["Breed"].str.replace("Doberman Pinsch","Doberman Pinscher")
datatest["Breed"]=datatest["Breed"].str.replace("Doberman Pinsch","Doberman Pinscher") 
data["Breed"]=data["Breed"].str.replace("Domestic Medium Hair","Domestic Mediumhair")
datatest["Breed"]=datatest["Breed"].str.replace("Domestic Medium Hair","Domestic Mediumhair")  
data["Breed"]=data["Breed"].str.replace("Boykin Span","Boykin Spaniel")
datatest["Breed"]=datatest["Breed"].str.replace("Boykin Span","Boykin Spaniel") 
data["Breed"]=data["Breed"].str.replace("Cavalier Span","Cavalier Spaniel")
datatest["Breed"]=datatest["Breed"].str.replace("Cavalier Span","Cavalier Spaniel")  
data["Breed"]=data["Breed"].str.replace("Dachshund Wirehair","Dachshund Wirehaired")
datatest["Breed"]=datatest["Breed"].str.replace("Dachshund Wirehair","Dachshund Wirehaired")    

breed=data.ix[:,3].str.split("/",expand=True)
breedtest=datatest.ix[:,2].str.split("/",expand=True)
breed.columns=["Breed","Cross"]
breedtest.columns=["Breed","Cross"]

# Mix
breed["Mix"]="No"
mixindex=(breed["Breed"].str.contains("Mix")==True)
breed.ix[mixindex,"Mix"]="Yes"
breed.ix[mixindex,"Breed"]=breed.ix[mixindex,"Breed"].str.replace(" Mix","")

breedtest["Mix"]="No"
mixindex=(breedtest["Breed"].str.contains("Mix")==True)
breedtest.ix[mixindex,"Mix"]="Yes"
breedtest.ix[mixindex,"Breed"]=breedtest.ix[mixindex,"Breed"].str.replace(" Mix","")

# Cross
breed.ix[np.array(pd.isnull(breed.ix[:,1])==True),1]=breed.ix[np.array(pd.isnull(breed.ix[:,1])==True),0]
breedtest.ix[np.array(pd.isnull(breedtest.ix[:,1])==True),1]=breedtest.ix[np.array(pd.isnull(breedtest.ix[:,1])==True),0] 

# Weight
breedweight=weight.groupby(weight["name"]).mean()
breedname=pd.Series(breedweight.index)
breedweight=np.array(breedweight)

for i in xrange(len(breedname)):
    breed.ix[breed["Breed"]==breedname[i],"Weight"]=float(breedweight[i])
    breedtest.ix[breedtest["Breed"]==breedname[i],"Weight"]=float(breedweight[i])   
    breed.ix[breed["Cross"]==breedname[i],"Weight"]=breed.ix[breed["Cross"]==breedname[i],"Weight"]+breedweight[i]
    breedtest.ix[breedtest["Cross"]==breedname[i],"Weight"]=breedtest.ix[breedtest["Cross"]==breedname[i],"Weight"]+breedweight[i]

breed["Weight"]=breed["Weight"]/float(2)
breedtest["Weight"]=breedtest["Weight"]/float(2)
    
    
# Drop Breed in Data
data=data.drop("Breed", axis=1)
datatest=datatest.drop("Breed", axis=1)

### Color ###
# replace 
data["Color"]=data["Color"].str.replace("Blue Cream","Bluecream")
datatest["Color"]=datatest["Color"].str.replace("Blue Cream","Bluecream")
data["Color"]=data["Color"].str.replace("Blue/Cream","Bluecream")
datatest["Color"]=datatest["Color"].str.replace("Blue/Cream","Bluecream")
data["Color"]=data["Color"].str.replace("Lynx Point","Lynxpoint")
datatest["Color"]=datatest["Color"].str.replace("Lynx Point","Lynxpoint")

# color matrix
color=data.ix[:,3].str.split("/",expand=True)
colortest=datatest.ix[:,2].str.split("/",expand=True)
color.columns=["Color1","Color2"]
colortest.columns=["Color1","Color2"]

# Color2
color.ix[np.array(pd.isnull(color.ix[:,1])==True),1]=color.ix[np.array(pd.isnull(color.ix[:,1])==True),0]
colortest.ix[np.array(pd.isnull(colortest.ix[:,1])==True),1]=colortest.ix[np.array(pd.isnull(colortest.ix[:,1])==True),0]

# Drop Color in Data
data=data.drop("Color", axis=1)
datatest=datatest.drop("Color", axis=1)

### Collect the Data ###
clean_data= pd.concat([data,dttime,sex,age,breed,color],axis=1)
clean_data_test= pd.concat([datatest,dttimetest,sextest,agetest,breedtest,colortest],axis=1)

##### Convert to Categorical Data
## AnimalType
enc = LabelEncoder()
enc.fit(pd.concat([clean_data["AnimalType"],clean_data_test["AnimalType"] ],axis=0))
clean_data["AnimalType"]=enc.transform(clean_data["AnimalType"])
clean_data_test["AnimalType"]=enc.transform(clean_data_test["AnimalType"])

## Outcometype
enc = LabelEncoder()
enc.fit(pd.concat([clean_data["OutcomeType"]],axis=0))
clean_data["OutcomeType"]=enc.transform(clean_data["OutcomeType"])

# Fertility
enc.fit(pd.concat([clean_data["Fertility"],clean_data_test["Fertility"]],axis=0))
clean_data["Fertility"]=enc.transform(clean_data["Fertility"])
clean_data_test["Fertility"]=enc.transform(clean_data_test["Fertility"])

# Sex
enc.fit(pd.concat([clean_data["Sex"],clean_data_test["Sex"]],axis=0))
clean_data["Sex"]=enc.transform(clean_data["Sex"])
clean_data_test["Sex"]=enc.transform(clean_data_test["Sex"])

# Mix
enc.fit(pd.concat([clean_data["Mix"],clean_data_test["Mix"]],axis=0))
clean_data["Mix"]=enc.transform(clean_data["Mix"])
clean_data_test["Mix"]=enc.transform(clean_data_test["Mix"])

# Breed
enc.fit(pd.concat([clean_data["Breed"],clean_data_test["Breed"],clean_data["Cross"],clean_data_test["Cross"]],axis=0))
clean_data["Breed"]=enc.transform(clean_data["Breed"])
clean_data_test["Breed"]=enc.transform(clean_data_test["Breed"])
clean_data["Cross"]=enc.transform(clean_data["Cross"])
clean_data_test["Cross"]=enc.transform(clean_data_test["Cross"])

#Color
enc.fit(pd.concat([clean_data["Color1"],clean_data_test["Color1"],clean_data["Color2"],clean_data_test["Color2"]],axis=0))
clean_data["Color1"]=enc.transform(clean_data["Color1"])
clean_data_test["Color1"]=enc.transform(clean_data_test["Color1"])
clean_data["Color2"]=enc.transform(clean_data["Color2"])
clean_data_test["Color2"]=enc.transform(clean_data_test["Color2"])


## Save data
### Save Data ###
clean_data.to_pickle("clean_data.pkl") 
clean_data_test.to_pickle("clean_datatest.pkl") 



etime = float(time.time()-stime)