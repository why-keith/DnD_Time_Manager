import PySimpleGUI as sg
from time import sleep
from os import listdir, mkdir
from database_class import db, pickler
from sys import exit
import custom_themes

QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'

icon_path="dnd_logo.ico"

def alert_box(text="TEXT HERE", window_name="ALERT", button_text="OK", sound=True, theme=None):
    sg.theme(theme)
    layout=[
            [sg.Text("  "+text+"  ")],
            [sg.Button(button_text)]
            ]
    window=sg.Window(window_name, layout, finalize=True, icon=icon_path, element_justification="center", force_toplevel=True,disable_minimize=True, return_keyboard_events=True, )
    if sound==True:
        print("\a")
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return
        elif event==button_text or event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            window.close()
            return
            

def choice_box(text, window_name="", theme=None):
    sg.theme(theme)
    layout=[
            [sg.Text(text)],
            [sg.Button("Yes"), sg.Button("No")]
            ]
    window=sg.Window(window_name, layout, finalize=True, icon=icon_path, element_justification="center", force_toplevel=True,disable_minimize=True, )
    print("\a")
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return False
        elif event=="No":
            window.close()
            return False
        elif event=="Yes":
            window.close()
            return True
        
def create_campaign(first=False, theme=None):
    sg.theme(theme)
    layout=[
            [sg.Text("New Campaign")],
            [sg.HorizontalSeparator(color="gray")],
            [sg.Text("Name"), sg.InputText("", size=(25,1), key="campaign_name")],
            [sg.Button("Create")]
            ]
    window=sg.Window("New...", layout, finalize=True, icon=icon_path, element_justification="center", force_toplevel=True,disable_minimize=False, return_keyboard_events=True, )

    while True:
        event, values = window.read()
        focused_enter=None
     #   print(event)
        if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            active_element=window.FindElementWithFocus()          #Dectects if the enter key has been pressed and checks which element is active
            print(active_element)
            
            if active_element==window["campaign_name"]:
                focused_enter="campaign_name"

        
        if event == sg.WIN_CLOSED and first==False:
            window.close()
            return 
        elif event == sg.WIN_CLOSED and first==True:
            window.close()
            exit()
            return
        
        elif event=="Create" or focused_enter=="campaign_name":
            name=window["campaign_name"].Get()
            
            try:
                if name in listdir("campaigns"):
                    alert_box(text="Campaign \"{}\" already exists".format(name))
                    pass
                else:
                    _dir="campaigns/{}".format(name)
                    
                    new_db=db()
                    mkdir(_dir)
                    pickler(_dir+"/{}.pkl".format(name), new_db)
                    
                    window.close()
                    return name
            except:
                alert_box(text="\"{}\" is not a valid campaign name".format(name))
                pass
                
def pref_window(pref, theme=None, using_RAW=False):
    sg.theme(theme)
  #  themes=["Default", "Black", "DarkRed1", "SandyBeach"]
    #themes=["Black", "BlueMono", "BluePurple", "BrightColors", "BrownBlue", "Dark", "Dark2", "DarkAmber", "DarkBlack", "DarkBlack1", "DarkBlue", "DarkBlue1", "DarkBlue10", "DarkBlue11", "DarkBlue12", "DarkBlue13", "DarkBlue14", "DarkBlue15", "DarkBlue16", "DarkBlue17", "DarkBlue2", "DarkBlue3", "DarkBlue4", "DarkBlue5", "DarkBlue6", "DarkBlue7", "DarkBlue8", "DarkBlue9", "DarkBrown", "DarkBrown1", "DarkBrown2", "DarkBrown3", "DarkBrown4", "DarkBrown5", "DarkBrown6", "DarkGreen", "DarkGreen1", "DarkGreen2", "DarkGreen3", "DarkGreen4", "DarkGreen5", "DarkGreen6", "DarkGrey", "DarkGrey1", "DarkGrey2", "DarkGrey3", "DarkGrey4", "DarkGrey5", "DarkGrey6", "DarkGrey7", "DarkPurple", "DarkPurple1", "DarkPurple2", "DarkPurple3", "DarkPurple4", "DarkPurple5", "DarkPurple6", "DarkRed", "DarkRed1", "DarkRed2", "DarkTanBlue", "DarkTeal", "DarkTeal1", "DarkTeal10", "DarkTeal11", "DarkTeal12", "DarkTeal2", "DarkTeal3", "DarkTeal4", "DarkTeal5", "DarkTeal6", "DarkTeal7", "DarkTeal8", "DarkTeal9", "Default", "Default1", "DefaultNoMoreNagging", "Green", "GreenMono", "GreenTan", "HotDogStand", "Kayak", "LightBlue", "LightBlue1", "LightBlue2", "LightBlue3", "LightBlue4", "LightBlue5", "LightBlue6", "LightBlue7", "LightBrown", "LightBrown1", "LightBrown10", "LightBrown11", "LightBrown12", "LightBrown13", "LightBrown2", "LightBrown3", "LightBrown4", "LightBrown5", "LightBrown6", "LightBrown7", "LightBrown8", "LightBrown9", "LightGray1", "LightGreen", "LightGreen1", "LightGreen10", "LightGreen2", "LightGreen3", "LightGreen4", "LightGreen5", "LightGreen6", "LightGreen7", "LightGreen8", "LightGreen9", "LightGrey", "LightGrey1", "LightGrey2", "LightGrey3", "LightGrey4", "LightGrey5", "LightGrey6", "LightPurple", "LightTeal", "LightYellow", "Material1", "Material2", "NeutralBlue", "Purple", "Reddit", "Reds", "SandyBeach", "SystemDefault", "SystemDefault1", "SystemDefaultForReal", "Tan", "TanBlue", "TealMono", "Topanga"]
    themes=custom_themes.themes
    theme_len=0
    for i in themes:
        if len(i)>theme_len:
            theme_len=len(i)
    
    
    layout=[
            [sg.Text("Appearance")],
            [sg.HorizontalSeparator()],
            [sg.Text("Theme (requires restart)"), sg.Combo(themes, key="themes", size=(theme_len+2, 1), default_value=theme)],
            [sg.Text("RAW Weather"),sg.Checkbox("", default=using_RAW, key="RAW_weather")],
            [sg.Button("Save"), sg.Button("Cancel")],
            ]
    window=sg.Window("Preferences", layout, finalize=True, icon=icon_path, element_justification="center", force_toplevel=True,disable_minimize=False)
  
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Cancel":
            save=False
            break
        
        elif event=="Save":
            save=True
            if window["themes"].Get() in themes:
                pref["new_theme"]=window["themes"].Get()
            using_RAW=window["RAW_weather"].get()
                
            
            
                
            print(pref["theme"])
            break
        
    window.close()        
    return pref, save, using_RAW
            
    
def rename_window(old_name, theme=None):
    sg.theme(theme)
    layout=[
            [sg.Text("Rename Campaign - "+old_name)],
            [sg.HorizontalSeparator(color="gray")],
            [sg.Text("New name"), sg.InputText("", size=(25,1), key="campaign_name")],
            [sg.Button("Confirm"), sg.Button("Cancel")]
            ]
    
    window=sg.Window("Rename", layout, finalize=True, icon=icon_path, element_justification="center", force_toplevel=True,disable_minimize=False, return_keyboard_events=True)
  
    while True:
        event, values = window.read()
        
        focused_enter=None
     #   print(event)
        if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            active_element=window.FindElementWithFocus()          #Dectects if the enter key has been pressed and checks which element is active
            print(active_element)
            
            if active_element==window["campaign_name"]:
                focused_enter="campaign_name"
        
        if event == sg.WIN_CLOSED or event=="Cancel":
            window.close()
            return 

        elif event=="Confirm" or focused_enter=="campaign_name":
            name=window["campaign_name"].Get()
            if name!="" and name not in listdir():
                window.close()
                return name
            else:
                if name in listdir():                 
                    alert_box(text="Campaign \"{}\" already exists".format(name))
                    pass
                
                
def set_reminder(theme=None): #UNDER CONSTRUCTON
    sg.theme(theme)

    layout=[
           # [sg.Text("test")],
            #[sg.HorizontalSeparator(color="gray")],
            [sg.Text("Name"), sg.InputText("", size=(25,1), key="campaign_name")],
            [sg.Text("Time until..."), sg.InputText("0", size=(5,1), key="hour_input", tooltip="Hour"), sg.InputText("0", size=(5,1), key="day_input", tooltip="Day")]
            [sg.Button("Confirm"), sg.Button("Cancel")],
     
            ]
    
    window=sg.Window("Preferences", layout, finalize=True, icon=icon_path, element_justification="center", force_toplevel=True,disable_minimize=False)
  
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
                
def test_window(theme=None):
    sg.theme(theme)
  #  c1=[sg.Button("Confirm"), sg.Button("Cancel")]
    layout=[
            [sg.Text("test")],
            [sg.HorizontalSeparator(color="gray")],
            [sg.Text("New name"), sg.InputText("", size=(25,1), key="campaign_name")],
            #[sg.Button("Confirm"), sg.Button("Cancel")],
     
            ]
    
    window=sg.Window("Preferences", layout, finalize=True, icon=icon_path, element_justification="center", force_toplevel=True,disable_minimize=False)
  
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
    
if __name__=="__main__":  
                    
    set_reminder()