import PySimpleGUI as sg

import json
from threading import Thread
import sys

from comms import CommsSender, CommsListener

commsListener = None
prevQueueState = []

creds = {
    "exchange": "2dgame",
    "port": "5672",
    "host": "crappy2d.us",
    "user": "player-1",
    "password": "horse1CatDonkey",
}


def checkMq():
    global commsListener
    global prevQueueState
    if len(commsListener.mq) == 0:
        return

    print(f"Receiving: {commsListener.mq[-1]}")
    return commsListener.mq.pop(-1)


def isJson(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


def sendMessage(tgt, cmd, bdy):
    if isJson(bdy):
        bdy = json.loads(bdy)  # turn it into json if you need to "access" it.

    if tgt == "everyone" or cmd == "broadcast":
        tgt = "broadcast"

    # create an instance of the sender code sending in appropriate
    # user/password along with which channel to message
    commsSender = CommsSender(**creds)

    # actually send the message
    commsSender.send(tgt, json.dumps({"cmd": cmd, "bdy": bdy}))


def listenForMessages():
    global commsListener

    # tell rabbitMQ which 'topics' you want to listen for. In this case anything
    # with the team name in it (user) or the broadcast keyword. Remember the pound
    # sign is a wildcard for rabbitMQ
    commsListener.bindKeysToQueue([f"#.{creds['user']}.#", "#.broadcast.#"])

    # now really start listening
    commsListener.startConsuming()


def main(player, offset):
    global commsListener
    creds["user"] = player
    commsListener = CommsListener(**creds)

    Thread(
        target=listenForMessages,
        args=(),
        daemon=True,
    ).start()

    sg.theme("DarkGrey14")

    commands = ("message", "broadcast", "move", "fire")
    targets = ("player-1", "player-2", "player-3", "Everyone")

    layout = [
        [sg.Text("Comms Output....", size=(40, 1))],
        [sg.Output(size=(88, 20), text_color="green", font="Courier 12")],
        [
            sg.Push(),
            sg.Text("Command:", size=(15, 1)),
            sg.Text("Target:", size=(15, 1)),
            sg.Text("Command Body:", size=(15, 1)),
            sg.Text("", size=(25, 1)),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.Combo(
                commands,
                size=(15, len(commands)),
                key="-COMMAND-",
                enable_events=True,
                default_value="message",
            ),
            sg.Combo(
                targets,
                size=(15, len(targets)),
                key="-TARGET-",
                enable_events=True,
                default_value="everyone",
            ),
            sg.Multiline(
                size=(40, 3),
                key="-CMDBODY-",
                enable_events=True,
                default_text="",
                # default_text='{"lat":123.345,"lon":34.234}',
            ),
            sg.Button("Submit"),
            sg.Push(),
        ],
    ]

    if offset:
        location = (offset, 330)
    else:
        location = (0, 0)

    window = sg.Window(f"Comms Panel: {creds['user']}", layout, location=location)

    while True:
        event, values = window.read(timeout=1000)
        if event == "EXIT" or event == sg.WIN_CLOSED:
            break  # exit button clicked
        if event == "Submit":
            # sp = sg.execute_command_subprocess("pip", "list", wait=True)
            cmd = values["-COMMAND-"]
            tgt = values["-TARGET-"]
            bdy = values["-CMDBODY-"]
            Thread(
                target=sendMessage,
                args=(
                    tgt,
                    cmd,
                    bdy,
                ),
                daemon=True,
            ).start()
        checkMq()

    window.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        player = "player-1"
    else:
        player = sys.argv[1]

    if len(sys.argv) == 3:
        offset = sys.argv[2]
    else:
        offset = None
    main(player, offset)
