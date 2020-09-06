import pickle
from random import choice, randint
import condition_lists as conditions

########################################################

def init():
    print("Initalising database...")
    day_data={"day_raw":0,
          "day": 1,
          "hour":0,
          "tenday":1,
          "month":[1,conditions.months[1]],
          "year":1491,
          "precipitation": choice(conditions.precipitation),
          "wind_dir": choice(conditions.wind_dir),
          "windspeed": choice(conditions.wind_speed),
          "temperature": choice(conditions.temp)
          } 
    pickle.dump( day_data, open("db.pkl", "wb"))

def save():
    try:
        pickle.dump( db, open("db.pkl", "wb"))
    except:
        print("UNABLE TO SAVE DATABASE")
    else:
        print("Database saved")
    

def show_all():
    for i in db:
       print("{}: {}".format(i,db[i]))
       
def next_day(days=1):
    for i in range(abs(days)):
        x=[randint(0,5) for i in range(4)]
        if x[0]==0:
            db["precipitation"]=choice(conditions.precipitation)
        if x[1]==0:
            db["wind_dir"]=choice(conditions.wind_dir)
        if x[2]==0:
            db["windspeed"]=choice(conditions.wind_speed)
        if x[3]==0:
            db["temperature"]=choice(conditions.temp)
    
    db["day"]=db["day_raw"]%30+1
    db["tenday"]=int((db["day_raw"]%30)/10)+1
    m=int((db["day_raw"]%360)/30)+1
    db["month"]=[m,conditions.months[m]]
    db["year"]=int(db["day_raw"]/360)+1491
    
    
def day(x):
    #x=input("Enter number of days to pass:\n>>")
    try:
        db["day_raw"]+=int(x)
        if int(x)!=0:
            next_day(int(x))
            
    except TypeError as e:
        print("INVALID TIME INCREMENT")
       
def hour(x):
   # x=input("Enter number of hours to pass:\n>>")
    try:
        db["hour"]+=int(x)
        while db["hour"]>=24:
            db["hour"]-=24
            db["day_raw"]+=1
            next_day()
        while db["hour"]<0:
            db["hour"]+=24
            db["day_raw"]-=1
            next_day(-1)
        print("Time: {}:00".format(db["hour"]))
    except TypeError as e:
        print("INVALID TIME INCREMENT")



def commands(cmd):
    try:
        cmd_dict[cmd]()
    except KeyError as e:
        print("INVALID COMMAND")
        
        
cmd_dict={"show":show_all,
          "hour":hour,
          "day":day,
          "save":save
          }
        
###########################################################

try:
    db=pickle.load(open( "db.pkl", "rb" ) )
except:
    init()    
    db=pickle.load(open( "db.pkl", "rb" ) )

#while 1:    
#    x=input("Enter command:\n>>")
#    commands(x)
