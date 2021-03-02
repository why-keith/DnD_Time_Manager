import PySimpleGUI as sg
from os import startfile, listdir, rename, mkdir, rmdir, getenv
from os.path import abspath, exists
#from time import sleep
from error import error
import window_layouts as popup
from database_class import pickler, unpickle, time_comparison
from database_class import db as db_class
from default_pref import default_pref  
from tkinter import Tk
from tkinter.filedialog import askdirectory
from send2trash import send2trash
from urllib.request import urlopen
from shutil import copyfile, copytree
from sys import exit

VERSION="v0.9.0"    
DEV_MODE=True

# Functions--------------------------------------------------------------------

def version_compare(ver, current_ver=VERSION):
    """
    Checks with a given version against that of the program

    Parameters
    ----------
    ver : str
        The version to be compared (form: "vX.Y.Z").

    Returns
    -------
    up_to_date : bool
        Whether the input version is up to date with the current version.

    """
    int_ver=[int(ver[1:].split(".")[i]) for i in range(len(ver[1:].split(".")))]
    new_int_ver=[int(current_ver[1:].split(".")[i]) for i in range(len(current_ver[1:].split(".")))]
 #   print(int_ver,new_int_ver)
    up_to_date=True
    for i in range(len(int_ver)):
       # print(int_ver[i],new_int_ver[i])
        if int_ver[i]<new_int_ver[i]:
            
            up_to_date=False
            break
        elif int_ver[i]>new_int_ver[i]:
            break
    #print(up_to_date)
    return up_to_date


def update_db(db):
    """
    Updates a database created in an old version by porting its attributes 
    into a new replacement database if required

    Parameters
    ----------
    db : <class 'database_class.db'>
        The old database to be updated.

    Returns
    -------
    new_db : <class 'database_class.db'>
        The new up-to-date database.

    """
    
    try:
        db_version=db.version
    except AttributeError:
        db_version="v0.0.0"
    if version_compare(db_version)==False:
        try:
            print("Updating database from {} to {}".format(db.version, VERSION))
        except:
            print("Updating database to {}".format(VERSION))
            
        attributes=[a for a in dir(db) if not a.startswith('__') and not callable(getattr(db, a))]
        new_db=db_class()
        for i in attributes:
            try:
                setattr(new_db,i, getattr(db,i)) 
            except Exception as e:
                error(e)
    
        if "month_raw" not in attributes:  #fixes introduction of month_raw
            try:
                new_db.month_raw=db.month[0]-1
                new_db.change_day(1)  #forces update
                new_db.change_day(-1)
            except Exception as e:
                error(e)
                
        new_db.version=VERSION
        pickler(camp_dir+"/"+campaign+".pkl", new_db)
        return new_db        
    
    else:
        return db

def update_menu():
    """
    Updates the elements of the menu bar
    
    Returns
    -------
    menu_dict : dictionary
        The updated menu.

    """

    global recent_camps, menu_dict, window
    
    recent_camps=pref["last campaign"][0:3]
    menu_dict={
        "File": ["New campaign...::new_campaign", "Open...::open_campaign", "Open recent", recent_camps, "Rename campaign::rename_campaign", "Delete campaign::delete_campaign", "Open save directory...::save_directory", "Preferences::preferences"],
        "Tools":["Get raw time::raw_time_out", "Set session no.::set_session_no", "Set reminder::set_reminder", "View reminders::view_reminders"],
        "Help": ["About::about", "ReadMe::readme", "Source Code::source_code"]
      }
    try:
        window["menu_bar"].Update(menu_definition=[[i,menu_dict[i]] for i in menu_dict])
    except NameError: 
        pass
    
    return menu_dict

def move_files(target_path):
    try:
        copytree("campaigns",abspath(target_path+"/campaigns"))
    except Exception as e:
        error(e)
    try:
        copyfile("pref.pkl", abspath(target_path+"/pref.pkl"))
    except Exception as e:
        error(e)

    return

def end_session():
    log=open("{}/{}.txt".format(camp_dir,campaign), "a")
    log.write("End of session {} ------------------------------------------------------\n".format(db.session_num))
    log.close()
    db.session_num+=1
    pickler(camp_dir+"/"+campaign+".pkl", db)

# Preferences & campaign loading-----------------------------------------------
if DEV_MODE==False:
    user_area=abspath(getenv('LOCALAPPDATA')+"/JP-Carr/DnD_Time_Manager")
else:
    user_area=abspath(getenv('LOCALAPPDATA')+"/JP-Carr/DnD_Time_Manager_DEV")

if version_compare(VERSION, current_ver="v0.9.0")==False:    
    if popup.alert_box(text="Moving campaign and preference files to user area\nFiles will be located at:\n"+user_area, window_name="Moving files", theme="Default")==True:
        print("moving files...")
        move_files(user_area)
    else:
        exit()

if "pref.pkl" in listdir(user_area):      #Loads pref file or creates new one
    pref=unpickle(user_area+"/pref.pkl")    
else:
    pref=default_pref
    pref["version"]=VERSION
    pickler(user_area+"/pref.pkl", pref)
    print("new pref file created")

#print(pref["version"])
if pref["version"]!=VERSION:      # updates pref file with any new entries
    for key in default_pref:
            if key not in pref:
                pref[key]=default_pref[key]
    pref["version"]=VERSION
    
    
if "campaigns" not in listdir(user_area):
    mkdir(user_area+"/campaigns")
    
campaign=None
if len(listdir(user_area+"/campaigns"))!=0:    #loads most recent possible campaign
    for i in pref["last campaign"]:
        if i in listdir(user_area+"/campaigns") and exists(user_area+"/campaigns/{}/{}.pkl".format(i, i)):
            campaign=i
            break
        
if campaign==None:
    for file in listdir(user_area+"/campaigns"):
        if exists(user_area+"/campaigns/{}/{}.pkl".format(file, file)):
            campaign=file
#print(campaign)        
if len(listdir(user_area+"/campaigns"))==0 or campaign==None:
    campaign=popup.create_campaign(user_area ,first=True, theme=pref["theme"])

pref["last campaign"].insert(0, campaign)
pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))
recent_camps=pref["last campaign"][0:3]
pickler(user_area+"/pref.pkl", pref)    
    
#print(pref["last campaign"])
#print(campaign)  
camp_dir=user_area+"/campaigns/"+campaign

  
db=unpickle(camp_dir+"/"+campaign+".pkl")   
db=update_db(db)

#db.reminders=[]

# Window design----------------------------------------------------------------

sg.theme(pref["theme"])
QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'
focused_enter=None
restart=False

menu_dict=update_menu()
#print(pref["show_tenday"])
main_layout=[
        [sg.Menu([[i,menu_dict[i]] for i in menu_dict], visible=False, key="menu_bar")],
        
        [sg.Text("Time")],
       
        [sg.InputText("{}:00".format(db.hour),size=(6,1), readonly=True,key="hour_display", tooltip="Time - 24 hour"),   sg.InputText(db.day, size=(3,1), readonly=True,key="day_display", tooltip="Day of the month"),   sg.InputText(db.tenday, size=(2,1), readonly=True,key="tenday_display", tooltip="Tenday", visible=pref["show_tenday"]),   sg.InputText("{}. {}".format(db.month[0],db.month[1]), size=(30,1), readonly=True,key="month_display", tooltip="Month"),   sg.InputText(db.year, size=(5,1), readonly=True,key="year_display", tooltip="Year - DR")],
        
        [sg.Text("Temperature"), sg.InputText(db.temperature, size=(20,1), readonly=True,key="temp_display"), sg.Text("Precipitation"), sg.InputText(db.precipitation, size=(6,1), readonly=True,key="precip_display")],
        
        [sg.Text("Wind Speed"), sg.InputText(db.windspeed, size=(6,1), readonly=True,key="WS_display"), sg.Text("Wind Direction"), sg.InputText(db.wind_dir, size=(3,1), readonly=True,key="WD_display")],
       
        [sg.HorizontalSeparator( pad=((0,0),(8,4)))],
       
        [sg.Text("Time Adjustment"), sg.InputText("0", size=(5,1), key="hour_input", tooltip="Hour Change"), sg.InputText("0", size=(5,1), key="day_input", tooltip="Day Change"), sg.Button("Submit"), sg.VerticalSeparator(color="gray", ),  sg.Button("End Session")],
        
        [sg.InputText(size=(40,1), key="log_input", tooltip="Log Input"), sg.Button("Log"), sg.VerticalSeparator(color="gray"), sg.Button("Open Log")]
        ]

updatable=["hour_display", "day_display", "tenday_display", "month_display", "year_display"]+["temp_display", "precip_display"]+["WS_display", "WD_display"]

if DEV_MODE==False:
    window_title="D&D Time Manager - "+campaign
else:
    window_title="DEV - D&D Time Manager - "+campaign
print("-----------------------------------")
window=sg.Window(window_title, main_layout, finalize=True, icon="dnd_logo.ico", return_keyboard_events=True)
print("-----------------------------------")

# Event loop-------------------------------------------------------------------

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
            error("Unable to print to {}.txt - PermissionError".format(campaign))
            
        except Exception as e:
            error("Unable to print to {}.txt".format(campaign)+str(e))
            
            
    elif event == "Open Log":  #opens log file
        try:
            startfile(abspath("{}/{}.txt".format(camp_dir,campaign)))
            
        except Exception as e:
            print(e)
            try:
                log=open("{}/{}.txt".format(camp_dir,campaign), "a")
                log.close()
                startfile(abspath("{}/{}.txt".format(camp_dir,campaign)))

            except Exception as e2:
                error("Unable to create {}.txt".format(campaign)+str(e2))
    
    elif event == "Submit" or focused_enter=="time":  #Sumbits changes to database time and updates day conditions
        
        
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
            for i in range(len(updatable)):
                window[updatable[i]].Update(update_values[i])
        window["hour_input"].Update("0")
        window["day_input"].Update("0")
        
        to_remove=[]
        for i in db.reminders:
            
            print(i[0])
            if time_comparison(db.time_data(),i[1]):
                to_remove.append(i)
                popup.alert_box(text=i[0], window_name="Reminder", theme=pref["theme"])
        for i in to_remove:
            print("removing "+i[0])
            db.reminders.remove(i)
        print(db.reminders)
        
    elif event == "End Session":
        end_session()     
        
# Menu Events -----------------------------------------------------------------
    
    # File --------------------------------------------------------------------
    elif event.endswith("::new_campaign"):
        old_campaign=campaign
        campaign=popup.create_campaign(user_area, first=False, theme=pref["theme"])
        
        if campaign!=None:
            print(campaign)
            camp_dir=user_area+"/campaigns/"+campaign
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
            pickler(user_area+"/pref.pkl", pref)

        else:
            campaign=old_campaign


    elif event.endswith("::open_campaign"):
        Tk().withdraw()
        try:
            path=askdirectory(initialdir=user_area+"/campaigns")#, title='Please select a directory')
        
        except Exception as e:
            print("Invalid Folder Path\n")
            print(e)
            pass
        
      #  else:
      #  print(path)
        if path=="":
              print("Invalid Folder Path\n")
              continue

        try:
            for file in listdir(path):
                print(file)
                if file.endswith(".pkl"):
                    print(file)
                    campaign=file.split(".")[0]
                    camp_dir=user_area+"/campaigns/"+campaign
                    db=unpickle(path+"/"+file) 
                    db=update_db(db)
                    update_values=["{}:00".format(db.hour), db.day, db.tenday, "{}. {}".format(db.month[0],db.month[1]), db.year]+[db.temperature, db.precipitation]+[db.windspeed, db.wind_dir]
                    break
        except Exception as e:
            error(e)
        
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
            pickler(user_area+"/pref.pkl", pref)
            
        

    elif event.endswith("::rename_campaign"):
        
        new_campaign=popup.rename_window(campaign, theme=pref["theme"])
        if new_campaign!=None:
            try:
                mkdir(user_area+r"/campaigns/{}".format(new_campaign))
                for file in listdir(camp_dir):
                    file_type=file.split(".")[-1]
                    rename(r"{}/{}".format(camp_dir,file), user_area+r"/campaigns/{}/{}.{}".format(new_campaign,new_campaign,file_type))
            except FileExistsError as e:
                popup.alert_box(text="Capaign \"{}\" already exists".format(new_campaign), theme=pref["theme"])
            except Exception as e:
                popup.alert_box(text="Unable to rename capaign", theme=pref["theme"])
                print(e)
            else:
                rmdir(camp_dir)
                old_campaign=campaign
                campaign=new_campaign
                camp_dir=user_area+"/campaigns/"+campaign
                window.set_title("D&D Time Manager - "+campaign)
                pref["last campaign"].insert(0, campaign)
                pref["last campaign"].remove(old_campaign)
                pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))

                update_menu()
                pickler(user_area+"/pref.pkl", pref)
                popup.alert_box(text="Rename sucessful", sound=False, window_name="Rename", theme=pref["theme"])
            
            
            
    elif event.endswith("::delete_campaign"):
        if popup.choice_box(text="Are you sure you want to delete campaign \"{}\"?".format(campaign), window_name="Delete Campaign", theme=pref["theme"])==True:
            send2trash(camp_dir)
            pref["last campaign"].remove(campaign)
            popup.alert_box(text="Campaign deleted", sound=False, window_name="Delete Campaign", theme=pref["theme"])
            if len(listdir(user_area+"/campaigns"))!=0: #loads most recent possible campaign
                for i in pref["last campaign"]:
                    if i in listdir(user_area+"/campaigns") and exists(user_area+"/campaigns/{}/{}.pkl".format(i, i)):
                        campaign=i
                        break
                    
            if campaign==None:
                for file in listdir(user_area+"/campaigns"):
                    if exists(user_area+"/campaigns/{}/{}.pkl".format(file, file)):
                        campaign=file
            print(campaign)        
            if len(listdir(user_area+"/campaigns"))==0 or campaign==None:
                campaign=popup.create_campaign(user_area, first=True, theme=pref["theme"])
            
            pref["last campaign"].insert(0, campaign)
            pref["last campaign"]=list(dict.fromkeys(pref["last campaign"]))

            update_menu()
            pickler(user_area+"/pref.pkl", pref)    
                
            print(pref["last campaign"])
            print(campaign)  
            camp_dir=user_area+"/campaigns/"+campaign            
            
            window.set_title("D&D Time Manager - "+campaign)
            db=unpickle(camp_dir+"/"+campaign+".pkl") 
            db=update_db(db)
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
            pickler(user_area+"/pref.pkl", pref)
            
       
    elif event.endswith("::save_directory"):
        startfile(user_area+"/campaigns")
    
    
    elif event.endswith("::preferences"):
        new_pref, save, db = popup.pref_window(pref, db, theme=pref["theme"])
        if save==True:
            pref=new_pref
            pickler(user_area+"/pref.pkl", pref)
            
       #     db.RAW=raw_weather
            pickler(camp_dir+"/"+campaign+".pkl", db)
     #       print("tenday -" +str(pref["show_tenday"]))

    # Tools--------------------------------------------------------------------
        
    elif event.endswith("::raw_time_out"):
        print(db.day_raw,db.hour)
        popup.alert_box(text="{} hours, {} days\n(This value can be accessed from the error log)".format(db.hour,db.day_raw), window_name="Raw Time", sound=False, theme=pref["theme"])
        error("Raw time request - {} hours, {} days".format(db.hour,db.day_raw), sound=False)
        
    #elif event.endswith("::set_session_no"):
     #   _=popup.change_session_num(db)

    elif event.endswith("::set_reminder"):
        time_data=(window["hour_display"].get(), window["day_display"].get(), window["month_display"].get(), window["year_display"].get() )
        remind_data,pref=popup.set_reminder(time_data, pref, theme=pref["theme"])
        if remind_data !=False:
            db.reminders.append(remind_data)
            pickler(camp_dir+"/"+campaign+".pkl", db)
            pickler("pref.pkl", pref)
            print(db.reminders)
            
    elif event.endswith("::view_reminders"):
        time_data=(window["hour_display"].get(), window["day_display"].get(), window["month_display"].get(), window["year_display"].get() )
        if popup.view_reminders(db, time_data, theme=pref["theme"])=="set_reminder":
            remind_data=popup.set_reminder(time_data, theme=pref["theme"])
            if remind_data !=False:
                db.reminders.append(remind_data)
                print(db.reminders)
        pickler(camp_dir+"/"+campaign+".pkl", db)
    
    # Help---------------------------------------------------------------------    

    elif event.endswith("::about"):
        if DEV_MODE==False:
            about_text="D&D Time Manager\nVersion: {}".format(VERSION)
        else:
            about_text="D&D Time Manager\nVersion: {} - DEV".format(VERSION)
        popup.alert_box(text=about_text, window_name="About", button_text="Close", sound=False, theme=pref["theme"])
    
    
    elif event.endswith("::readme"):
        try:
            _=urlopen("https://github.com/")
        except:
            startfile("README.md")
        else:
            startfile("https://github.com/JP-Carr/DnD_Time_Manager/blob/master/README.md")
    

    elif event.endswith("::source_code"):
        try:
            _=urlopen("https://github.com/")
            
        except:
            popup.alert_box(text="Unable to reach github.com")
            
        else:
            startfile("https://github.com/JP-Carr/DnD_Time_Manager")  
     
    # Recent campaigns---------------------------------------------------------    
     
    elif event in recent_camps:
        print(event)
        if event!=campaign:
           # print(0)
            
            try:
                for file in listdir(user_area+"/campaigns/"+event):
                    if file.endswith(".pkl"):
                        camp_dir=user_area+"/campaigns/"+event
                        campaign=file.split(".")[0]
                        db=unpickle(camp_dir+"/"+file) 
                        db=update_db(db)
                        update_values=["{}:00".format(db.hour), db.day, db.tenday, "{}. {}".format(db.month[0],db.month[1]), db.year]+[db.temperature, db.precipitation]+[db.windspeed, db.wind_dir]
                        break
            except FileNotFoundError:
                pref["last campaign"].remove(event)
                update_menu()
                popup.alert_box("Unable to load campaign \"{}\"".format(event), theme=pref["theme"])
                
            except Exception as e:
                error(e)
            
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
                pickler(user_area+"/pref.pkl", pref)
    
  #  else:
   #     print (event)  

# End of loop------------------------------------------------------------------
if pref["end_session_on_close"]==True and DEV_MODE==False:
    end_session()

pref["theme"]=pref["new_theme"]   
pickler(user_area+"/pref.pkl", pref)
window.close()