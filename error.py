from datetime import datetime

def error(message, sound=True):
    message=str(message)
    print(message)
    error_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if sound:
        print("\a")
    with open("error_log.txt", "a") as error_log:
        error_log.write(f"{error_time} | {message}\n")
    return
