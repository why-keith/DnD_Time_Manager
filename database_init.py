import pickle
day_data={"day": 1,
          "hour":1,
          "precipitation": "None",
          "wind_dir": "SW",
          "windspeed": "None"
          } 

#print(day_data)

pickle.dump( day_data, open("db.pickle", "wb"))

#x=pickle.load(open( "save.pickle", "rb" ) )

#print(x)