import PySimpleGUI as sg
import console_test as ct

"""
sg.theme('DarkAmber')	# Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText("inout",readonly=True)],
            [sg.Button('Ok'), sg.Button('Cancel'), sg.Button("Save")] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    if event=="Save":
        print("saved")
    if event=="Ok":
        print('You entered ', values[0])
        layout[1][1].update(value="ewatwe")
    
    
    print(event)
window.close()
"""
"""
x=0
layout=[
        [sg.Text("Time"), sg.InputText(str(x), readonly=True,key="number")],
        [sg.Button("+1",key="+1"), sg.Button("-1",key="-1")]
        ]

window=sg.Window("Test",layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        print("asdf")
        break
    elif event=="+1":
        x+=1
        window["number"].Update(str(x))
        #layout[0][1].Update(str(x))
    elif event=="-1":
        x-=1
        layout[0][1].Update(str(x))
    
window.close()

"""

layout=[
        [sg.Text("Time")],
       
        [sg.InputText("{}:00".format(ct.db["hour"]),size=(10,1), readonly=True,key="hour_display"), sg.InputText(ct.db["day"], size=(7,1), readonly=True,key="day_display"), sg.InputText(ct.db["tenday"], size=(10,1), readonly=True,key="tenday_display"), sg.InputText("{}. {}".format(ct.db["month"][0],ct.db["month"][1]), size=(30,1), readonly=True,key="month_display"), sg.InputText(ct.db["year"], size=(5,1), readonly=True,key="year_display")],
        
        [sg.Text("Temperature"), sg.InputText(ct.db["temperature"], size=(20,1), readonly=True,key="temp_display"), sg.Text("Precipitation"), sg.InputText(ct.db["precipitation"], size=(6,1), readonly=True,key="precip_display")],
        
        [sg.Text("Wind Speed"), sg.InputText(ct.db["windspeed"], size=(6,1), readonly=True,key="WS_display"), sg.Text("Wind Direction"), sg.InputText(ct.db["wind_dir"], size=(3,1), readonly=True,key="WD_display")],
       
        [sg.InputText("0", size=(5,1), key="hour_input"), sg.InputText("0", size=(5,1), key="day_input"), sg.Button("Submit")]
        ]

#updatable=[i for i in layout[1]]+[layout[2][1], layout[2][3]]+[layout[3][1], layout[3][3]]
updatable=["hour_display", "day_display", "tenday_display", "month_display", "year_display"]+["temp_display", "precip_display"]+["WS_display", "WD_display"]
update_values=["{}:00".format(ct.db["hour"]), ct.db["day"], ct.db["tenday"], "{}. {}".format(ct.db["month"][0],ct.db["month"][1]), ct.db["year"]]+[ct.db["temperature"], ct.db["precipitation"]]+[ct.db["windspeed"], ct.db["wind_dir"]]
window=sg.Window("D&D Time Tracker",layout, finalize=True)
#print(len(updatable), len(update_values))
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "Submit":
        try:
            h=int(window["hour_input"].Get())
            d=int(window["day_input"].Get())
        except:
            print("INVALID ENTRY")
            pass
        else:
            ct.hour(h)
            ct.day(d)
            ct.save()
            update_values=["{}:00".format(ct.db["hour"]), ct.db["day"], ct.db["tenday"], "{}. {}".format(ct.db["month"][0],ct.db["month"][1]), ct.db["year"]]+[ct.db["temperature"], ct.db["precipitation"]]+[ct.db["windspeed"], ct.db["wind_dir"]]
            ct.show_all()
            print("\n")
            for i in range(len(updatable)):
                window[updatable[i]].Update(update_values[i])
            window["hour_input"].Update("0")
            window["day_input"].Update("0")
    

    
    
window.close()