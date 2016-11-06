class train():
    def __init__(self):
        self.train_name        = 'X###N-#'
        self.train_type        = "T"
        self.direction         = "N"
        self.passenger      = 0.0
        self.intermodal     = 0.0
        self.unit           = 0.0
        self.pasns          = 0.0
        self.intls          = 0.0
        self.units          = 0.0
        self.distance       = 0.0
        self.avg_spd        = 0.0
        self.run_time       = 0.0
        self.total_delay    = 0.0
        self.termd_dwell    = 0.0
        self.day            = 0
        self.norm_delay     = 0
        
def write_train(T,sim_name):
    items = [T.name, T.avgspd, T.direct, T.type, T.norm_delay, T.day]
        
    string = ""
    for col in items:
        string = string + "," + str(col)
    return string[1:]+" \n"

def get_hr(time_str):
    if len(time_str.split(':'))==3:
        h, m, s = time_str.split(':')
        return int(h)+ int(m)/60 + int(s)/3600
    elif len(time_str.split(':'))==2:
        m, s = time_str.split(':')
        return int(m)/60 + int(s)/3600
    elif len(time_str.split(':'))==1:
        return int(time_str)/3600
    elif len(time_str.split(':'))==4:
        d, h, m, s = time_str.split(':')
        return 24*int(d)+int(h)+ int(m)/60 + int(s)/3600

def read_all(all_trains, simulation):
    report_file = open(simulation,'r')
    Train_List = {}
    counter = 0
    max_days_simulated = 0
    incomplete = -1
    ct=0
     
    for line in report_file:
        inc = line.find("DISPATCH NOT COMPLETE")
        if inc <>-1:
           incomplete = 1
        
        a= line.find("Statistics for included run-time trains")
        
        if counter>0:
            counter=counter+1

        if (a <> -1) and (counter == 0):
           counter = 1
           
        if ((counter>0) & (len(line)>170)):
            if (line[83] == "%") and (line[170]== "%"):
                New_Train = train ()
                New_Train.name     =line [6:line.index('-')].replace (" ", "")
                New_Train.type     = line[320:333].replace (" ", "")
                New_Train.direct   = line[343:347].replace (" ", "")
                New_Train.avgspd   = float (line[40:50].replace (" ", ""))
                New_Train.run_time = float (get_hr(line[65:78].replace (" ", "")))
                New_Train.total_delay = float (get_hr(line[155:165].replace (" ", "")))
                New_Train.day      = float(line[line.index('-')+1:line.index('-')+2].replace (" ", ""))
                New_Train.norm_delay = float(line[210:222].replace (" ", ""))
                Train_List[line[6:14].replace (" ", "")] = New_Train
                max_days_simulated = max (max_days_simulated, New_Train.day)

        if (counter >0) and (line.find('Case')<>-1): 
           counter =0
        
        if (counter>8) and (line.count('-')>300):
           counter=0


        ct+=1
           
    report_file.close()

    if incomplete <>-1:
        Last_day = float(max_days_simulated) -2
        I = "I-"
    else:
        Last_day = float(max_days_simulated)
        I = ""    
        
    for t in Train_List:
        day = Train_List[t].day
        if day<=Last_day:
            all_trains[t,I+simulation] = Train_List[t]
     
    return all_trains
            
#---------------------------- Main Porgram -----------------------------

      
all_trains = {}
sim='Kippen-R1'
name=sim+'.REPORT'
try:
    open (name,'r')  
    all_trains = read_all(all_trains,name)                        
    print "Read",sim
except IOError:
    z= 'do nothing'
               

Header_Row = "Name, Speed, Driection, Type, Delay_100_Mile, Day\n"
ofile = open(sim+'.csv','wb')
ofile.write(Header_Row)
for entry in all_trains:
    ofile.write(write_train(all_trains[entry], entry[1]))
ofile.close()
print "Done!"
