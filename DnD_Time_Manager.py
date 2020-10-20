import PySimpleGUI as sg
import console_test as ct
from os import startfile
from time import sleep
from error import error

QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'

focused_enter=None

#sg.theme("DarkRed1")

layout=[
        [sg.Text("Time")],
       
        [sg.InputText("{}:00".format(ct.db["hour"]),size=(6,1), readonly=True,key="hour_display", tooltip="Time - 24 hour"),   sg.InputText(ct.db["day"], size=(3,1), readonly=True,key="day_display", tooltip="Day of the month"),   sg.InputText(ct.db["tenday"], size=(2,1), readonly=True,key="tenday_display", tooltip="Tenday"),   sg.InputText("{}. {}".format(ct.db["month"][0],ct.db["month"][1]), size=(30,1), readonly=True,key="month_display", tooltip="Month"),   sg.InputText(ct.db["year"], size=(5,1), readonly=True,key="year_display", tooltip="Year - DR")],
        
        [sg.Text("Temperature"), sg.InputText(ct.db["temperature"], size=(20,1), readonly=True,key="temp_display"), sg.Text("Precipitation"), sg.InputText(ct.db["precipitation"], size=(6,1), readonly=True,key="precip_display")],
        
        [sg.Text("Wind Speed"), sg.InputText(ct.db["windspeed"], size=(6,1), readonly=True,key="WS_display"), sg.Text("Wind Direction"), sg.InputText(ct.db["wind_dir"], size=(3,1), readonly=True,key="WD_display")],
       
        [sg.Text("Time Adjustment"), sg.InputText("0", size=(5,1), key="hour_input", tooltip="Hour Change"), sg.InputText("0", size=(5,1), key="day_input", tooltip="Day Change"), sg.Button("Submit")],
        
        [sg.InputText(size=(40,1), key="log_input", tooltip="Log Input"), sg.Button("Log"), sg.Button("Open Log")]
        ]

updatable=["hour_display", "day_display", "tenday_display", "month_display", "year_display"]+["temp_display", "precip_display"]+["WS_display", "WD_display"]

window=sg.Window("D&D Time Manager", layout, finalize=True, icon="dnd_logo.ico", return_keyboard_events=True)




while True:
    event, values = window.read()
    
    if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
        active_element=window.FindElementWithFocus()          #Dectects if the enter key has been pressed and checks which element is active
        if active_element==window["log_input"]:
            focused_enter="log"
        elif active_element==window["hour_input"] or active_element==window["day_input"]:
            focused_enter="time"
  
    
    if event == sg.WIN_CLOSED:    #breaks loop if window is closed
        break
    
    elif event=="Log" or focused_enter=="log":    #submits log 
        focused_enter=None
        

        try:
            log=open("log.txt", "a")
            log.write("{} {}/{}/{} - {}\n".format(str(ct.db["hour"])+":00", ct.db["day"], ct.db["month"][0], ct.db["year"], window["log_input"].Get()))
            
            log.close()    
            window["log_input"].Update("")
            
        except PermissionError as e:
            print("UNABLE TO LOG")
            error("Unable to print to log.txt - "+str(e))
            
        except:
            print("UNABLE TO LOG")
            error("Unable to print to log.txt")
            
            
    elif event == "Open Log":  #opens log file
        try:
            startfile("log.txt")
        except:
            
            try:
                log=open("log.txt", "a")
                log.close()
                startfile("log.txt")
                
            except PermissionError as e:
                print("UNABLE TO LOG")
                error("Unable to print to log.txt - "+str(e))
            except:
                print("UNABLE TO OPEN LOG FILE")
                error("Unable to open log.txt")
    
    elif event == "Submit" or focused_enter=="time":  #Sumbits changes to database time and updates day conditions
        
        focused_enter=None
        
        try:
            h=int(window["hour_input"].Get())
            d=int(window["day_input"].Get())
        except:
            print("INVALID ENTRY")
            error("Invalid time input \"{}, {}\" detected".format(window["hour_input"].Get(),window["day_input"].Get()))
            pass
        else:
            ct.hour(h)
            ct.day(d)
            ct.save()
            update_values=["{}:00".format(ct.db["hour"]), ct.db["day"], ct.db["tenday"], "{}. {}".format(ct.db["month"][0],ct.db["month"][1]), ct.db["year"]]+[ct.db["temperature"], ct.db["precipitation"]]+[ct.db["windspeed"], ct.db["wind_dir"]]
      #      ct.show_all()
       #     print("\n")
            for i in range(len(updatable)):
                window[updatable[i]].Update(update_values[i])
        window["hour_input"].Update("0")
        window["day_input"].Update("0")    
    
    
    
   # else:
   #     print ("|{}|".format(event))  
       

window.close()