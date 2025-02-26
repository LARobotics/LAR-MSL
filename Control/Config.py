ToPrint = True

def Print(*args, **kwargs):
    if ToPrint:     print(*args, **kwargs)   # noqa: E701
    
FREQUENCY = 50

STOP = 0 
MOVE = 1
ATTACK = 2
KICK = 3
RECEIVE = 4
COVER = 5
DEFEND = 6
CONTROL = 7

import subprocess

def get_computer_name():
    try:
        result = subprocess.run(['hostname'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return None
    
    
ROBOT_NAME = get_computer_name()
try:
    ROBOT_ID = int(ROBOT_NAME[-1])
except:
    ROBOT_ID = 9
IP = f"172.16.49.1{ROBOT_ID}"
