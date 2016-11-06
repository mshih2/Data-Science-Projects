import csv
import random
import math
import numpy as np


##### Environmental Variables #####
time_sec_unit=0.5
n=40000
rand_lev=1   #departure randomness factor, 1 turn on 0 off
trip_lev=0   # trip randomnes factor, 1 turn on 0 off

##### Functions #####
# break overnight train
def breaktrain1(row):
    new_train=[0]*12
    new_train[1]=0
    new_train[2]=row[2]-24
    new_train[4]=startpoint(row[6],row[4],row[1])
    new_train[5]=0
    new_train[7]=row[0]
    new_train[0]=row[0]+'-n'
    new_train[3]=row[3]
    new_train[6]=row[6]
    new_train[8]=row[8]
    new_train[9]=0
    new_train[10]=0
    new_train[11]=0
    return (new_train)

def breaktrain2(row):
    new_train=[0]*12
    new_train[1]=24+row[1]
    new_train[2]=24
    new_train[4]=row[4]
    new_train[5]=0
    new_train[7]=row[0]
    new_train[0]=row[0]+'-n'
    new_train[3]=row[3]
    new_train[6]=row[6]
    new_train[8]=row[8]
    new_train[9]=0
    new_train[10]=0
    new_train[11]=0
    return (new_train)

# calculate start point for over night trains
def startpoint(spd, strpoint, dep):
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

##### Import Data #####
rawdata=[list(line) for line in csv.reader(open('C:\Users\Mei-Cheng Shih\Dropbox\Capacity Screening\Mainline-Conflict\Data-c.csv'))]
infra=[list(line) for line in csv.reader(open('C:\Users\Mei-Cheng Shih\Dropbox\Capacity Screening\Mainline-Conflict\Infrastructure.csv'))]
ddis=[list(line) for line in csv.reader(open('C:\Users\Mei-Cheng Shih\Dropbox\Capacity Screening\Mainline-Conflict\delay.csv'))]

repeat=np.shape(np.matrix(ddis))[1]

infra=infra[0]
infra_m=np.matrix([float(i) for i in infra])
infra_m=infra_m[0]
blok_num=len(infra)
spacing=np.zeros((blok_num,1))
for i in range(blok_num-1):
    spacing[i]=float(infra[i+1])-float(infra[i])
spacing=spacing[0]  

myinput=[]

for row in rawdata:
    row[1]=float(row[1])
    row[2]=float(row[2])
    row[4]=float(row[4])
    row[5]=float(row[5])
    row[6]=float(row[6])
    row[8]=float(row[8])
    row[9]=float(row[9])
    row[10]=float(row[10])
    row[11]=float(row[11])

# 0:No  1:Dep  2:Arr  3:Direc  4:SP  5:DR  6:Spd  7:OT  8:Pr  9:a  10:b  11:num  12: Total Distance

##### Simulation ######

# create temporal and spacial space sections
spac_sec=np.zeros((242,1))
spac_num=np.zeros((242,1))

for sec in range(1,242):
    spac_num[sec]=sec

tunit=int(24/time_sec_unit)
time_sec=np.matrix(np.zeros((tunit+1,1)))
time_num=np.zeros((tunit+1,1))

for sec in range(1,tunit):
    time_num[sec]=sec*time_sec_unit

zt_sec=np.zeros((tunit+1,blok_num))
zt_num=np.zeros((blok_num,1))
st_sec=np.zeros((tunit+1,242))


## d and t saving
d=[]
t=[]

##### Loop this part as simulation####
for i in range(1,n+1):
    print "The current progress is {a}".format(a=(round((i/float(n+1)),2)))
    # Equal to initial statement
    rounddata=[]
    overnight=[]
    ### So important!!!
    for row in rawdata:
        rounddata.append(list(row))

# generate actual departure time
    count=0
    for row in rounddata:
        #<-------------------------- RANDOM SWITCH
        if row[7]=='N':
            row[1]=row[1]+row[5]*random.uniform(-1, 1)*rand_lev
#            row[1]=row[1]
            row[2]=row[1]+242/float(row[6])+trip_lev*float(ddis[count][int(math.floor(random.uniform(0, repeat)))]) 
#            row[2]=row[1]+242/float(row[6])
            row[4]=row[4]
            row[6]= 242/float(row[2]-row[1])

        count+=1

    for row in rounddata:
    # create overnight train list
        if row[1]>24 and row[2]>24 and row[7]=='N':
            row[1]=row[1]-24
            row[2]=row[2]-24
        elif row[1]<24 and row[2]>24 and row[7]=='N':
            overnight.append(row[0]+'-n')
            rounddata.append(breaktrain1(row))
            row[2]=24
    # create previous night train list
        elif row[1]<0 and row[2]<0 and row[7]=='N':
            row[1]=24+row[1]
            row[2]=24+row[2]
        elif row[1]<0 and row[2]>0 and row[7]=='N':
            overnight.append(row[0]+'-n')
            rounddata.append(breaktrain2(row))
            row[4]=startpoint(row[6],row[4],row[1])
            row[1]=0 
   
# find linear lines
# S=Spd, D=SP, T=Dep
# East: a = S, b =D+ST
# West: a'= -S, b'=D-ST
# T*=(b'-b)/(a-a'), D*=a(T)+b
    count=0
    for row in rounddata:
        count=count+1
        if row[3]=='E':
            row[11]=count;
            row[9]=  row[6]
            row[10]= row[4]-row[9]*row[1]
        else:
            row[11]=count;
            row[9]=  -row[6]
            row[10]= row[4]-row[9]*row[1]

### intersect judgement ###
    conflict_t={}
    conflict_d={}

# intersect trains
    for row1 in rounddata:
        # set empty sets
        int_train=[]
        int_train_name=[]
        
        for row in rounddata:
            dsel=0
            tsel=0
            conflict_t=-1
            conflict_d=-1
            
            if (row1[0]!=row[0] and row1[9]!=row[9]):
                conflict_t=(row[10]-row1[10])/float(row1[9]-row[9])
                conflict_d=(row1[9]*(conflict_t)+row1[10]) 
                conflict_d2=(row[9]*(conflict_t)+row[10]) 

                if ((row[11]>row1[11]) and (conflict_t>0 and conflict_t<24) and (conflict_d>0 and conflict_d<242)):                  
                    dsel=int(math.floor(conflict_d))
                    tsel=int(math.floor(conflict_t/float(time_sec_unit))) 
                    spac_sec[dsel-1]+=1
                    time_sec[tsel-1]+=1
                    st_sec[tsel-1][dsel-1]+=1
# Zonal conflict calculation
                    k=np.zeros((blok_num))
                    il=np.amax(np.where(conflict_d>=infra_m[:])[1])
                    zt_sec[tsel-1][il]+=1
                                     
spac_sec=[round(x/float(n),5) for x in spac_sec]
time_sec=[round(x/float(n),5) for x in time_sec]

output_st_time=[0]*(tunit+1)*242
output_st_dis=[0]*(tunit+1)*242
output_st_con=[0]*(tunit+1)*242
peak_st=[0]*242

count=0
for sec1 in range(0,242):
    for sec2 in range(0,tunit+1):
        output_st_time[count]=sec2*time_sec_unit
        output_st_dis[count]=sec1
        output_st_con[count]=round(st_sec[sec2][sec1]/float(n),5)
        count=count+1

zt_st_count=[0]*21        
for i in xrange(blok_num):
    for sec2 in range(0,tunit+1):
        if round(zt_sec[sec2-1][i]/float(n),5)>zt_st_count[i]:
            zt_st_count[i]=round(zt_sec[sec2-1][i]/float(n),5)

de_max_dis=[0]*242
de_max_time=[0]*242
for sec1 in range(0,242):
    for sec2 in range(0,tunit+1):
        if round(st_sec[sec2][sec1]/float(n),5)>de_max_dis[sec1]:   
            de_max_dis[sec1]=round(st_sec[sec2][sec1]/float(n),5)
            de_max_time[sec1]=sec2*time_sec_unit
                
                        
output_zt_time=[0]*(tunit+1)*blok_num
output_zt_zone=[0]*(tunit+1)*blok_num
output_zt_con=[0]*(tunit+1)*blok_num
peak_st=[0]*242
count=0

for sec1 in xrange(blok_num):
    for sec2 in range(0,tunit+1):
        output_zt_time[count]=sec2*time_sec_unit
        output_zt_zone[count]=sec1
        output_zt_con[count]=round(zt_sec[sec2][sec1]/float(n),5)
        count=count+1

with open('C:\Users\Mei-Cheng Shih\Dropbox\Capacity Screening\Mainline-Conflict\space_result.csv', 'w') as csvfile:
    fieldnames = ['Num', 'Conflict','Density','Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\r')
    writer.writeheader()
    for i in range(0,242):
        writer.writerow({'Num':str(spac_num[i]) ,'Conflict':str(spac_sec[i]), 'Density':str(de_max_dis[i]), 'Time':str(de_max_time[i])})

with open('C:\Users\Mei-Cheng Shih\Dropbox\Capacity Screening\Mainline-Conflict\hour_result.csv', 'w') as csvfile:
    fieldnames = ['Num', 'Conflict']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\r')
    writer.writeheader()
    for i in range(0,(tunit+1)):
        writer.writerow({'Num':str(time_num[i]) ,'Conflict':str(time_sec[i])})

with open('C:\Users\Mei-Cheng Shih\Dropbox\Capacity Screening\Mainline-Conflict\st_result.csv', 'w') as csvfile:
    fieldnames = ['Time', 'Distance','Conflict']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\r')
    writer.writeheader()
    for i in range(0,(tunit+1)*242):
        writer.writerow({'Time':str(output_st_time[i]) ,'Distance':str(output_st_dis[i]),'Conflict':str(output_st_con[i])})
        
with open('C:\Users\Mei-Cheng Shih\Dropbox\Capacity Screening\Mainline-Conflict\zt_result.csv', 'w') as csvfile:
    fieldnames = ['Time', 'Zone','Conflict']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\r')
    writer.writeheader()
    for i in range(0,(tunit+1)*blok_num):
        writer.writerow({'Time':str(output_zt_time[i]) ,'Zone':str(output_zt_zone[i]),'Conflict':str(output_zt_con[i])})
        
with open('C:\Users\Mei-Cheng Shih\Dropbox\Capacity Screening\Mainline-Conflict\zt_max.csv', 'w') as csvfile:
    fieldnames = ['Conflict']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\r')
    writer.writeheader()
    for i in range(0,blok_num):
        writer.writerow({'Conflict':str(zt_st_count[i])})
        
with open('C:\Users\Mei-Cheng Shih\Dropbox\Capacity Screening\Mainline-Conflict\conflictd.csv', 'w') as csvfile:
    fieldnames = ['Conflict']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\r')
    writer.writeheader()
    for i in range(0,len(d)):
        writer.writerow({'Conflict':str(d[i])})

