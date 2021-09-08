from datetime import datetime

def error(message, sound=True):
    message=str(message)
    print(message)
    error_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if sound==True:
        print("\a")
    error_log=open("error_log.txt","a")
    error_log.write(error_time + " | " +message + "\n")
    error_log.close()
    return
    