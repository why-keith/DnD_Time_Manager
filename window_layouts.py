import PySimpleGUI as sg
from time import sleep
from os import listdir, mkdir
from database_class import db, pickler
from sys import exit

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
                
def pref_window(theme=None):
    themes=[None, "Black", "DarkRed1"]
    
    
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
        
        if event == sg.WIN_CLOSED:
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
                    
        elif event=="Cancel":
            window.close()
