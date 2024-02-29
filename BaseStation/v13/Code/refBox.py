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
    import consts
    STOP = consts.STOP
    MOVE = consts.MOVE
    ATTACK = consts.ATTACK
    KICK = consts.KICK
    RECIEVE = consts.RECIEVE
    COVER = consts.COVER
    DEFEND = consts.DEFEND
    CONTROL = consts.CONTROL
    FIELD_DIMENSIONS = consts.FIELD_DIMENSIONS

server_address = ('localhost', 28097)
message = {"team": "LAR@MSL"}
message_json = json.dumps(message)
refBoxCommands = ["START","STOP","DROP_BALL","HALF_TIME","END_GAME","GAME_OVER","PARK","FIRST_HALF","SECOND_HALF","FIRST_HALF_OVERTIME","SECOND_HALF_OVERTIME","RESET"," WELCOME","KICKOFF","FREEKICK","GOALKICK","THROWIN","CORNER","PENALTY","GOAL","SUBGOAL","REPAIR","YELLOW_CARD","DOUBLE_YELLOW","RED_CARD","SUBSTITUTION","IS_ALIVE"]

Message = ""
Arg = ""
CommandID = -1
myIPs = ["172.16.49.0", "172.16.49.1", "127.0.0.1", "224.16.32.127"]
state = 0

available = 0
try:
    refBoxSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    refBoxSocket.connect(server_address)
    refBoxSocket.settimeout(0.001)
    available = 1
except:
    print("NO REF BOX")
    pass
    

def handleComms():
    if available:
        try:
            refBoxSocket.sendall(message_json.encode())
            response = refBoxSocket.recv(1024).decode().replace("\n", "").replace("\x00", "")
            response_dict = json.loads(response)
            return checkMessage(response_dict)
        except Exception as e:
            if str(e) != "timed out" and str(e) != "[WinError 10053] An established connection was aborted by the software in your host machine":
                print(e)
    return -1, -1
        
def checkMessage(message):
    if message["command"] in refBoxCommands:
        return message["command"], message["targetTeam"]
    return "NONE", ""

def handleCommand(command, message, Robots):
    if command != -1:
        print(command, message)
        match command:
            case "NONE":        pass
            case "PENALTY":     return 2
            case "CORNER":      return 2
            case "THROWIN":     return 2
            case "GOALKICK":    return 2
            case "FREEKICK":    return 2
            case "KICKOFF":     return 2
            case "GOAL":        
                if message in myIPs: consts.SCORE[0] += 1
                else:                consts.SCORE[1] += 1
            case "DROPBALL":    return 2
            case "":            return state
            case "SIDE":        return 1
            case "PARK":        return 2
            case "STOP":        return 1
            case "START":       return 0
            case "RESET":       consts.SCORE = [0, 0]
    return state

if __name__ == "__main__":
    while(1):
        handleComms()

