from threading import Thread
import time
import os


os.system("sudo python3 /home/pi/sensorDataToDB.py")

os.system("sudo python /home/pi/iBeacon-Scanner-/to_db.py")
