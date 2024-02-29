import json
import socket

if __name__ == "__main__":
    FIELD_DIMENSIONS = {
        "A" : 180,
        "B" : 120,
        "C" : 69,
        "D" : 39,
        "E" : 22.5,
        "F" : 7.5,
        "G" : 7.5,
        "H" : 40,
        "I" : 36,
        "J" : 1.5,
        "K" : 1.25,
        "L" : 10,
        "M" : 10,
        "N" : 70,
        "O" : 10,
        "P" : 5,
        "Q" : 35,
    }
    
    STOP = 0
    MOVE = 1
    ATTACK = 2
    KICK = 3
    RECIEVE = 4
    COVER = 5
    DEFEND = 6
    CONTROL = 7
else:
    from consts import *

server_address = ('172.16.49.156', 28097)
message = {"team": "LAR@MSL"}
refBoxCommands = ["START","STOP","DROP_BALL","HALF_TIME","END_GAME","GAME_OVER","PARK","FIRST_HALF","SECOND_HALF","FIRST_HALF_OVERTIME","SECOND_HALF_OVERTIME","RESET"," WELCOME","KICKOFF","FREEKICK","GOALKICK","THROWIN","CORNER","PENALTY","GOAL","SUBGOAL","REPAIR","YELLOW_CARD","DOUBLE_YELLOW","RED_CARD","SUBSTITUTION","IS_ALIVE"]

Message = ""
CommandID = -1

message_json = json.dumps(message)


available = 0
try:
    refBoxSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # refBoxSocket.connect(server_address)
    # refBoxSocket.settimeout(0.001)
    # available = 1
except:
    pass
    

def handleComms():
    try:
        refBoxSocket.sendall(message_json.encode())
        response = refBoxSocket.recv(1024).decode().replace("\n", "").replace("\x00", "")
        response_dict = json.loads(response)
        return checkMessage(response_dict)
    except Exception as e:
        if str(e) != "timed out":
            print(e)
    return CommandID
        
def checkMessage(message):
    if message["command"] in refBoxCommands:
        print(message["command"], refBoxCommands.index(message["command"]))
        return refBoxCommands.index(message["command"])

def handleCommand(CommandID, Robots):
    
    if CommandID == refBoxCommands.index("STOP"):
        Robots[0].packet = [STOP, 0, 0, 0, 0, 0, 0]
        Robots[1].packet = [STOP, 0, 0, 0, 0, 0, 0]
        Robots[2].packet = [STOP, 0, 0, 0, 0, 0, 0]
        Robots[3].packet = [STOP, 0, 0, 0, 0, 0, 0]
        Robots[4].packet = [STOP, 0, 0, 0, 0, 0, 0]
    if CommandID == refBoxCommands.index("PARK"):
        Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
        Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
        Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
        Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
        Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]


if __name__ == "__main__":
    while(1):
        handleComms()

