from datetime import datetime

def error(message):
    error_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("\a")
    error_log=open("error_log.txt","a")
    error_log.write(error_time + " | " +message + "\n")
    error_log.close()
    return
    