import os
import time
os.system("gnome-terminal  -t \"Server Yolo\" --geometry 100x100+80+100 -- bash -c \"make server\"")
#os.system("make server")
time.sleep(15)
os.system("gnome-terminal -t Golang --geometry 100x100+1000+100 -- bash -c \"make debug\" ")
