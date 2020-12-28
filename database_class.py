import pickle
from random import choice, randint
import condition_lists as conditions
########################################################

class db:
    
    def __init__(self):
        print("Initalising database...")
        """
        self.day_data={"day_raw":0,
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
        """
        self.day_raw=0
        self.day=1
        self.hour=0
        self.tenday=1
        self.month=[1,conditions.months[1]]
        self.year=1491
        self.precipitation= choice(conditions.precipitation)
        self.wind_dir=choice(conditions.wind_dir)
        self.windspeed=choice(conditions.wind_speed)
        self.temperature= choice(conditions.temp)
        self.RAW=False
  #      pickle.dump( self.day_data, open("db.pkl", "wb"))
    """
    def save():
        try:
            pickle.dump( db, open("db.pkl", "wb"))
        except:
            print("UNABLE TO SAVE DATABASE")
        else:
            print("Database saved")
    """    
    
    def show_all(self):
        for i in db:
           print("{}: {}".format(i,self.day_data[i]))
           
    def next_day(self, days=1):
        if self.RAW==True:
            prob=0
        else:
            prob=5
     
        for i in range(abs(days)):
            x=[randint(0,prob) for i in range(4)]
            if x[0]==0:
                self.precipitation=choice(conditions.precipitation)
            if x[1]==0:
                self.wind_dir=choice(conditions.wind_dir)
            if x[2]==0:
                self.windspeed=choice(conditions.wind_speed)
            if x[3]==0:
                self.temperature=choice(conditions.temp)
        
        self.day=self.day_raw%30+1
        self.tenday=int((self.day_raw%30)/10)+1
        m=int((self.day_raw%360)/30)+1
        self.month=[m,conditions.months[m]]
        self.year=int(self.day_raw/360)+1491
        
        
    def change_day(self, x):
        #x=input("Enter number of days to pass:\n>>")
        try:
            self.day_raw+=int(x)
            if int(x)!=0:
                self.next_day(int(x))
                
        except TypeError as e:
            print("INVALID TIME INCREMENT")
           
    def change_hour(self, x):
       # x=input("Enter number of hours to pass:\n>>")
        try:
            self.hour+=int(x)
            while self.hour>=24:
                self.hour-=24
                self.day_raw+=1
                self.next_day()
            while self.hour<0:
                self.hour+=24
                self.day_raw-=1
                self.next_day(-1)
            print("Time: {}:00".format(self.hour))
        except TypeError as e:
            print("INVALID TIME INCREMENT")


def pickler(path,obj):
    outfile = open(path,'wb')
    pickle.dump(obj,outfile)
    outfile.close()
    print(path+" pickled")
    
def unpickle(path):
    try:    
        infile = open(path,'rb')
        obj = pickle.load(infile)
        infile.close()
        print(path+" unpickled")
        return obj
    except FileNotFoundError:
        return None

     
###########################################################
"""
try:
    db=pickle.load(open( "db.pkl", "rb" ) )
except:
    init()    
    db=pickle.load(open( "db.pkl", "rb" ) )

#while 1:    
#    x=input("Enter command:\n>>")
#    commands(x)
"""