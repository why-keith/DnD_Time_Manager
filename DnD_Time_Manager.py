import PySimpleGUI as sg
#import console_test as ct
from os import startfile, listdir, rename, mkdir, rmdir
from os.path import abspath, exists
from time import sleep
from error import error
import window_layouts as popup
from database_class import pickler, unpickle
from default_pref import new_pref
from tkinter import Tk
from tkinter.filedialog import askdirectory
from send2trash import send2trash
#import custom_themes

VERSION="v0.4.0 + DEV"

def update_menu():

    global recent_camps, menu_dict, window
    
    recent_camps=pref["last campaign"][0:3]
    menu_dict={
        "File": ["New campaign...::new_campaign", "Open...::open_campaign", "Open recent", recent_camps, "Rename campaign::rename_campaign", "Delete campaign::delete_campaign", "Open save directory...::save_directory", "Preferences::preferences"],
        "Help": ["About::about", "ReadMe::readme", "Source Code::source_code"]
      }
    try:
        window["menu_bar"].Update(menu_definition=[[i,menu_dict[i]] for i in menu_dict])
    except NameError: 
        pass
    
    return menu_dict


if "pref.pkl" in listdir():
    pref=unpickle("pref.pkl")
    
else:
    pref=new_pref
    pickler("pref.pkl", pref)
    print("new pref file created")
    
if "campaigns" not in listdir():
    mkdir("campaigns")
    
campaign=None
if len(listdir("campaigns"))!=0: #loads most recent possible campaign
    for i in pref["last campaign"]:
        if i in listdir("campaigns") and exists("campaigns/{}/{}.pkl".format(i, i)):
            campaign=i
            break
        
if campaign==None:
    for file in listdir("campaigns"):
        if exists("campaigns/{}/{}.pkl".format(file, file)):
            campaign=file
print(campaign)        
if len(listdir("campaigns"))==0 or campaign==None:
    campaign=popup.create_campaign(first=True, theme=pref["theme"])

pref["last campaign"].insert(0, campaign)
pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))
recent_camps=pref["last campaign"][0:3]
#window["menu_bar"].Update(menu_definition=[[i,menu_dict[i]] for i in menu_dict])
pickler("pref.pkl", pref)    
    
print(pref["last campaign"])
print(campaign)  
camp_dir="campaigns/"+campaign
    
db=unpickle(camp_dir+"/"+campaign+".pkl")    

#pref["theme"]="Fighter"

################################################################################

sg.theme(pref["theme"])
QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'
focused_enter=None

#menu_dict={
 #           "File": ["New campaign...::new_campaign", "Open...::open_campaign", "Open recent", recent_camps, "Rename campaign::rename_campaign", "Delete campaign::delete_campaign", "Open save directory...::save_directory", "Preferences::preferences"],
  #          "Help": ["About::about", "ReadMe::readme", "Source Code::source_code"]
   #       }

menu_dict=update_menu()

main_layout=[
        [sg.Menu([[i,menu_dict[i]] for i in menu_dict], visible=False, key="menu_bar")],
        
        [sg.Text("Time")],
       
        [sg.InputText("{}:00".format(db.hour),size=(6,1), readonly=True,key="hour_display", tooltip="Time - 24 hour"),   sg.InputText(db.day, size=(3,1), readonly=True,key="day_display", tooltip="Day of the month"),   sg.InputText(db.tenday, size=(2,1), readonly=True,key="tenday_display", tooltip="Tenday"),   sg.InputText("{}. {}".format(db.month[0],db.month[1]), size=(30,1), readonly=True,key="month_display", tooltip="Month"),   sg.InputText(db.year, size=(5,1), readonly=True,key="year_display", tooltip="Year - DR")],
        
        [sg.Text("Temperature"), sg.InputText(db.temperature, size=(20,1), readonly=True,key="temp_display"), sg.Text("Precipitation"), sg.InputText(db.precipitation, size=(6,1), readonly=True,key="precip_display")],
        
        [sg.Text("Wind Speed"), sg.InputText(db.windspeed, size=(6,1), readonly=True,key="WS_display"), sg.Text("Wind Direction"), sg.InputText(db.wind_dir, size=(3,1), readonly=True,key="WD_display")],
       
        [sg.Text("Time Adjustment"), sg.InputText("0", size=(5,1), key="hour_input", tooltip="Hour Change"), sg.InputText("0", size=(5,1), key="day_input", tooltip="Day Change"), sg.Button("Submit")],
        
        [sg.InputText(size=(40,1), key="log_input", tooltip="Log Input"), sg.Button("Log"), sg.VerticalSeparator(color="gray"), sg.Button("Open Log")]
        ]

updatable=["hour_display", "day_display", "tenday_display", "month_display", "year_display"]+["temp_display", "precip_display"]+["WS_display", "WD_display"]

window=sg.Window("D&D Time Manager - "+campaign, main_layout, finalize=True, icon="dnd_logo.ico", return_keyboard_events=True)



while True:
    event, values = window.read()
    focused_enter=None
    
    if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
       
        active_element=window.FindElementWithFocus()          #Dectects if the enter key has been pressed and checks which element is active
        if active_element==window["log_input"]:
            focused_enter="log"
        elif active_element==window["hour_input"] or active_element==window["day_input"]:
            focused_enter="time"
  
    
    if event == sg.WIN_CLOSED:    #breaks loop if window is closed
        break
    
    elif event=="Log" or focused_enter=="log":    #submits log 
        
        try:
            log=open("{}/{}.txt".format(camp_dir,campaign), "a")
            log.write("{} {}/{}/{} - {}\n".format(str(db.hour)+":00", db.day, db.month[0], db.year, window["log_input"].Get()))
            
            log.close()    
            window["log_input"].Update("")
            
        except PermissionError as e:
            print("UNABLE TO LOG - PermissionError")
            error("Unable to print to {}.txt - PermissionError".format(campaign))
            
        except Exception as e:
            print("UNABLE TO LOG")
            error("Unable to print to {}.txt".format(campaign)+str(e))
            
            
    elif event == "Open Log":  #opens log file
        try:
            startfile(abspath("{}/{}.txt".format(camp_dir,campaign)))
      #  except FileNotFoundError as e:            
       #error("Unable to open {}.txt".format(campaign)+str(e))
            
        except Exception as e:
            print(e)
            try:
                log=open("{}/{}.txt".format(camp_dir,campaign), "a")
                log.close()
                startfile(abspath("{}/{}.txt".format(camp_dir,campaign)))
                
           # except PermissionError as e2:
            #    print("UNABLE TO LOG FILE")
             #   error("Unable to open {}.txt".format(campaign)+str(e2))
            except Exception as e2:
                print(e2)
                print("UNABLE TO CREATE LOG FILE")
                error("Unable to create {}.txt".format(campaign)+str(e2))
    
    elif event == "Submit" or focused_enter=="time":  #Sumbits changes to database time and updates day conditions
        
      #  focused_enter=None
        
        try:
            h=int(window["hour_input"].Get())
            d=int(window["day_input"].Get())
        except:
            print("INVALID ENTRY")
            error("Invalid time input \"{}, {}\" detected".format(window["hour_input"].Get(),window["day_input"].Get()))
            pass
        else:
            db.change_hour(h)
            db.change_day(d)
            pickler(camp_dir+"/"+campaign+".pkl", db)
            update_values=["{}:00".format(db.hour), db.day, db.tenday, "{}. {}".format(db.month[0],db.month[1]), db.year]+[db.temperature, db.precipitation]+[db.windspeed, db.wind_dir]
      #      ct.show_all()
       #     print("\n")
            for i in range(len(updatable)):
                window[updatable[i]].Update(update_values[i])
        window["hour_input"].Update("0")
        window["day_input"].Update("0")
    
    
    
# Menu Events -----------------------------------------------------------------------
    
    elif event.endswith("::new_campaign"):
        campaign=popup.create_campaign(first=False, theme=pref["theme"])
        
        if campaign!=None:
            print(campaign)
            camp_dir="campaigns/"+campaign
            for file in listdir(camp_dir):
                    if file.endswith(".pkl"):
                        campaign=file.split(".")[0]
                        db=unpickle(camp_dir+"/"+file) 
                        update_values=["{}:00".format(db.hour), db.day, db.tenday, "{}. {}".format(db.month[0],db.month[1]), db.year]+[db.temperature, db.precipitation]+[db.windspeed, db.wind_dir]
                        break
            for i in range(len(updatable)):
                window[updatable[i]].Update(update_values[i])
            window.set_title("D&D Time Manager - "+campaign)
            window["hour_input"].Update("0")
            window["day_input"].Update("0")
            window["log_input"].Update("")
            
            pref["last campaign"].insert(0, campaign)
            pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))

            update_menu()
            pickler("pref.pkl", pref)




    elif event.endswith("::open_campaign"):
        Tk().withdraw()
        try:
            path=askdirectory(initialdir=abspath("")+"/campaigns")#, title='Please select a directory')
        except Exception as e:
            print("Invalid Folder Path\n")
            print(e)
            pass
        
        else:
            print(path)
            try:
                for file in listdir(path):
                    if file.endswith(".pkl"):
                        campaign=file.split(".")[0]
                        camp_dir="campaigns/"+campaign
                        db=unpickle(path+"/"+file) 
                        update_values=["{}:00".format(db.hour), db.day, db.tenday, "{}. {}".format(db.month[0],db.month[1]), db.year]+[db.temperature, db.precipitation]+[db.windspeed, db.wind_dir]
                        break
            except Exception as e:
                print(e)
            
            else:        
                for i in range(len(updatable)):
                    window[updatable[i]].Update(update_values[i])
                window.set_title("D&D Time Manager - "+campaign)
                window["hour_input"].Update("0")
                window["day_input"].Update("0")
                window["log_input"].Update("")
                
                pref["last campaign"].insert(0, campaign)
                pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))

                update_menu()
                pickler("pref.pkl", pref)
            
        if path=="":
            print("Invalid Folder Path\n")
            pass

    elif event.endswith("::rename_campaign"):
        
        new_campaign=popup.rename_window(campaign, theme=pref["theme"])
        if new_campaign!=None:
            try:
                mkdir(r"campaigns/{}".format(new_campaign))
                for file in listdir(camp_dir):
                    file_type=file.split(".")[-1]
                    rename(r"{}/{}".format(camp_dir,file), r"campaigns/{}/{}.{}".format(new_campaign,new_campaign,file_type))
            except Exception as e:
                popup.alert_box(text="Unable to rename capaign", theme=pref["theme"])
                print(e)
            else:
                rmdir(camp_dir)
                old_campaign=campaign
                campaign=new_campaign
                camp_dir="campaigns/"+campaign
                window.set_title("D&D Time Manager - "+campaign)
                pref["last campaign"].insert(0, campaign)
                pref["last campaign"].remove(old_campaign)
                pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))

                update_menu()
                pickler("pref.pkl", pref)
                popup.alert_box(text="Rename sucessful", sound=False, window_name="Rename", theme=pref["theme"])
            
            
            
    elif event.endswith("::delete_campaign"):
        if popup.choice_box(text="Are you sure you want to delete campaign \"{}\"?".format(campaign), window_name="Delete Campaign", theme=pref["theme"])==True:
            send2trash(camp_dir)
            pref["last campaign"].remove(campaign)
            popup.alert_box(text="Campaign deleted", sound=False, window_name="Delete Campaign", theme=pref["theme"])
            if len(listdir("campaigns"))!=0: #loads most recent possible campaign
                for i in pref["last campaign"]:
                    if i in listdir("campaigns") and exists("campaigns/{}/{}.pkl".format(i, i)):
                        campaign=i
                        break
                    
            if campaign==None:
                for file in listdir("campaigns"):
                    if exists("campaigns/{}/{}.pkl".format(file, file)):
                        campaign=file
            print(campaign)        
            if len(listdir("campaigns"))==0 or campaign==None:
                campaign=popup.create_campaign(first=True, theme=pref["theme"])
            
            pref["last campaign"].insert(0, campaign)
            pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))

            update_menu()
            pickler("pref.pkl", pref)    
                
            print(pref["last campaign"])
            print(campaign)  
            camp_dir="campaigns/"+campaign            
            
            window.set_title("D&D Time Manager - "+campaign)
            db=unpickle(camp_dir+"/"+campaign+".pkl")   
            update_values=["{}:00".format(db.hour), db.day, db.tenday, "{}. {}".format(db.month[0],db.month[1]), db.year]+[db.temperature, db.precipitation]+[db.windspeed, db.wind_dir]
                    
            for i in range(len(updatable)):
                window[updatable[i]].Update(update_values[i])
            window.set_title("D&D Time Manager - "+campaign)
            window["hour_input"].Update("0")
            window["day_input"].Update("0")
            window["log_input"].Update("")
     
            
            pref["last campaign"].insert(0, campaign)
            pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))

            update_menu()
            pickler("pref.pkl", pref)
            
       
    elif event.endswith("::save_directory"):
        startfile("campaigns")
    
    
    elif event.endswith("::preferences"):
        pref, save_pref = popup.pref_window(pref, theme=pref["theme"])
        if save_pref==True:
            pickler("pref.pkl", pref)
        #print(pref["theme"])
        
    
    elif event.endswith("::about"):
        about_text="D&D Time Manager\nVersion: {}".format(VERSION)
        popup.alert_box(text=about_text, window_name="About", button_text="Close", sound=False, theme=pref["theme"])
    
    
    elif event.endswith("::readme"):
        try:
            startfile("https://github.com/JP-Carr/DnD_Time_Manager/blob/master/README.md")  
        except:
            try:
                startfile("README.md")
            except:
                pass
    

    elif event.endswith("::source_code"):
        try:
            startfile("https://github.com/JP-Carr/DnD_Time_Manager")  
        except:
            pass
     
        
    elif event in recent_camps:
        print(event)
        if event!=campaign:
            print(0)
            
            try:
                #camp_dir="campaigns/"+event
                for file in listdir("campaigns/"+event):
                    if file.endswith(".pkl"):
                        camp_dir="campaigns/"+event
                        campaign=file.split(".")[0]
                        db=unpickle(camp_dir+"/"+file) 
                        update_values=["{}:00".format(db.hour), db.day, db.tenday, "{}. {}".format(db.month[0],db.month[1]), db.year]+[db.temperature, db.precipitation]+[db.windspeed, db.wind_dir]
                        break
            except FileNotFoundError:
                pref["last campaign"].remove(event)
                update_menu()
                popup.alert_box("Unable to load campaign \"{}\"".format(event), theme=pref["theme"])
                
            except Exception as e:
                print(e)
            
            else:
                for i in range(len(updatable)):
                    window[updatable[i]].Update(update_values[i])
                window.set_title("D&D Time Manager - "+campaign)
                window["hour_input"].Update("0")
                window["day_input"].Update("0")
                window["log_input"].Update("")
                
                pref["last campaign"].insert(0, campaign)
                pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))

                update_menu()
                pickler("pref.pkl", pref)
    
  #  else:
   #     print (event)  
       
pref["theme"]=pref["new_theme"]   
pickler("pref.pkl", pref)
window.close()