# D&D Time Manager
D&D Time Manager is a simple application created for Microsoft Windows to allow Dungeon Masters to keep track of in-game events and the times at which they occurred. It also automates the rolling of local weather conditions as outlined in ch. 5 of the Dungeon Master's Guide (with a few small tweaks).

## Installation
At present D&DTM is only available as a standalone .zip archive for Microsoft Windows. Download the [Latest Release](https://github.com/JP-Carr/DnD_Time_Manager/releases/latest), simply unzip the archive in your chosen directory and you're good to go. If you are updating from and old version of D&DTM, ensure you do not erase/overwrite your database (db.pkl) and your log file (log.txt) unless you want a fresh install.

## Usage
To start the program, run "DnD_Time_Manager.exe". This will present you with the app's GUI:
![GUI_v0.5.0](https://github.com/JP-Carr/DnD_Time_Manager/blob/media/Images/GUI/v0.7.0/GUI_0.7.0_Default.JPG)
#### Layout
* Row 1 - In-game time: Time(hh:mm), Day, Tenday, Month, Year
* Row 2 - Temperature and precipitation level
* Row 3 - Wind Speed and direction
* Row 4 - Hour change input, Day change input, Submit time change (change can be any positive or negative integer)
* Row 5 - Log input box, Enter log, open log.txt
-----------------------------------
Entering values in the time input boxes and clicking "Submit" will update the in-game time. Weather conditions are automatically rolled on a day change.
The "Log" function allows for notes to be recorded from the GUI, the log is stored alongside the in-game time and date for easy reference.

### Campaigns
Each campaign is handled separately and can be edited and switched between at will. 

## Updating to v0.7.0
Campaign databases created in older version are incompatible with v0.7.0.
For each campaign:
1. Backup the log file 
2. Note down the raw time value from "Tools" → "Get raw time" (if running v0.6.0)
3. Update to v0.7.0
4. Create a new campaign to replace the old one
5. Enter the raw time to bring the campaign time up to date
6. Access the campaign directory through: File → Open save directory... → [campaign name]
7. Place the backed up log file in the campaign directory, ensuring the name of the file matches that of the directory

## Updating to v0.5.0
Due to the changes to campaigns, updating to v0.5.0 while keeping saved data requires further steps to work correctly.
1. Backup db.pkl and log.txt from your install directory to a separate location
2. Replace the old install with the new release version
3. Run "DnD_Time_Manager.exe" and name your campaign
4. Click "Open Log" to ensure a log file exists for this campaign
5. Access the campaign directory through: File → Open save directory... → [campaign name]
6. Replace the pkl and txt files found in this directory with the ones backed up in Step 1. Ensure that the old files renamed to match the newly created ones.
7. Close and reopen "DnD_Time_Manager.exe"

## Disclaimer
This is an unofficial piece of software and is in no way endorsed or sponsored by [Wizards of the Coast](https://company.wizards.com/)
