import os

dev_mode=os.path.exists(".gitignore")

if dev_mode:
    user_area=os.path.abspath(os.getenv('LOCALAPPDATA')+"/JP-Carr/DnD_Time_Manager_DEV")
else:
    user_area=os.path.abspath(os.getenv('LOCALAPPDATA')+"/JP-Carr/DnD_Time_Manager")
    