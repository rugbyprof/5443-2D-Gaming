"""
Example sender with some helper code to format and parse commands 
"""

from comms import CommsSender
import json
import sys


def isJson(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


def help():
    print("=" * 60)
    print("Commands are formatted like the following examples: ")
    print("    targetplayer ~ command ~ json object of command info")
    print("Examples: ")
    print('    player-1 ~ fire ~ {"lon":97.234,"lat":33.456,"ammo":"explosive_round"}')
    print('    player-2 ~ message ~ "You are going down"')
    print('    everyone ~ broadcast ~ "Message to everyone: player-1 is going down!"')
    print('    everyone ~ move ~ "X":234,"Y":110,"direction":"ENE"')
    print("The tildes (~) are used as an easy character to split on!")
    print("=" * 60)


def parseCommand(cmdTxt):
    print(cmdTxt)
    target = None
    cmd = None
    data = None

    target, cmd, data = cmdTxt.split("~")

    target = target.strip()
    cmd = cmd.strip()
    data = data.strip()
    if isJson(data):
        data = json.loads(data)  # turn it into json if you need to "access" it.

    if target == "everyone" or cmd == "broadcast":
        target = "broadcast"

    return {"target": target, "cmd": cmd, "data": data}


creds = {
    "exchange": "2dgame",
    "port": "5672",
    "host": "crappy2d.us",
    "user": "player-2",
    "password": "horse1CatDonkey",
    "hash": None,
}

team = creds["user"]
commsSender = CommsSender(**creds)
txt = 1

while txt:
    txt = input("Enter ['command','quit','help']:")
    if txt == "help":
        help()
    elif txt == "quit":
        print("quitting...")
        break
    else:
        cmd = parseCommand(txt)
        print(cmd)

        # turn the json back into a string to send it
        commsSender.sendCommand(cmd["target"], json.dumps(cmd))

commsSender.closeConnection()
