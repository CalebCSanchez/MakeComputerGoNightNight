
import datetime
import time


import os





print("Enter how many minutes you'd like to sleep")


timeout =int(input())
timeoutHours = timeout / 60
timeoutMinutes = timeout % 60
print("Computer will fall asleep in" + str(round(timeoutHours, 2)) +" hours at "+ str(datetime.datetime.now() + datetime.timedelta(hours = int(timeoutHours), minutes = timeoutMinutes)))

time.sleep(timeout * 60)
os.system("shutdown.exe /h")


print("goodnight :)")