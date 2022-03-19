import globals as gb
import sqlite3

class db_manager:
    
    def __init__(self):
        self.db_path=gb.user_area+"\\DnDTM.db"
        pass #set up db if not exist
    
    def get_pref(self, pref):
        cmd=f"SELECT value FROM preferences WHERE preference = {pref}"