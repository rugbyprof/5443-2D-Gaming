"""
"""
import json
import os
import sys
import time

import pika
import random
from threading import Thread


from rich import print


class Comms(object):
    """A helper class for client to client messaging. I don't know anything about
    pub/sub so this is rudimentary. In fact, it probably doesn't need to be a
    class! However, I organized it into one simply for encapsulation, keeping
    data and methods together and the added bonus of a constructor etc.
    """

    _messageQueue = {}

    def __init__(self, **kwargs):
        """Remember keyword arguments are params like: key=arg so order doesn't matter.
            The following example shows you how to init an instance of this class.
        Example:
            {
                "exchange": "2dgame",
                "port": "5672",
                "host": "crappy2d.us",
                "user": "yourteamname",
                "password": "yourpassword",
            }
        """
        self.exchange = kwargs.get("exchange", None)
        self.port = kwargs.get("port", 5432)
        self.host = kwargs.get("host", None)
        self.user = kwargs.get("user", None)
        self.password = kwargs.get("password", None)
        self.binding_keys = kwargs.get("binding_keys", [])

        if not self.user in self._messageQueue:
            self._messageQueue[self.user] = []

        self.establishConnection()

    def establishConnection(self, **kwargs):
        """This method basically authenticates with the message server using:

                host, port, user, and password

        After authentication it chooses which "exchange" to listen to. This
        is just like a "channel" in slack. The exchange "type" = "topic" is
        what allows us to use key_bindings to choose which messages to recieve
        based on keywords.
        """
        self.exchange = kwargs.get("exchange", self.exchange)
        self.port = kwargs.get("port", self.port)
        self.host = kwargs.get("host", self.host)
        self.user = kwargs.get("user", self.user)
        self.password = kwargs.get("password", self.password)

        names = ["exchange", "port", "host", "user", "password"]
        params = [self.exchange, self.port, self.host, self.user, self.password]
        for p in zip(names, params):
            if not p[1]:
                print(
                    f"Error: connection parameter `{p[0]}` missing in class Comms method `establishConnection`!"
                )
                sys.exit()

        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            self.host, int(self.port), self.exchange, credentials
        )

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic")


class CommsListener(Comms):
    def __init__(self, **kwargs):
        """Extends Comms"""
        self.binding_keys = kwargs.get("binding_keys", [])

        super().__init__(**kwargs)

    def bindKeysToQueue(self, binding_keys=None):
        """https://www.rabbitmq.com/tutorials/tutorial-five-python.html

        A binding key is a way of "subscribing" to a specific messages. Without
        getting to the difference between "routing" and "topics" I will say topics
        should work better for battleship. Valid topics are things like:

           python.javascript.cpp

        This topic would receive any messages from queues containing the routing
        keys: `python` or `javascript` or `cpp`. You can register as many keys as you like.
        But you can also use wild cards:

            * (star) can substitute for exactly one word.
            # (hash) can substitute for zero or more words.

        So if you want to get all messages with your team involved:
            teamname.#
        Or if you want all messages that fire at you:
            teamname.fire.#
        Or if you want to send a message to everyone:
            broadcast.#

        Follow the link above to get a better idea, but at minimum you should
        add binding keys for anything with your teamname (or maybe id) in it.

        """
        result = self.channel.queue_declare("", exclusive=True)
        self.queue_name = result.method.queue

        if binding_keys == None and len(self.binding_keys) == 0:
            self.binding_keys = ["#"]
        elif binding_keys:
            self.binding_keys = binding_keys

        for binding_key in self.binding_keys:
            # print(binding_key)
            self.channel.queue_bind(
                exchange=self.exchange, queue=self.queue_name, routing_key=binding_key
            )

    def startConsuming(self, callback=None):
        if not callback:
            callback = self.callback
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        """This method gets run when a message is received. You can alter it to
        do whatever is necessary.
        """
        self._messageQueue[self.user].append(f"{method.routing_key} : {body}")
        print(self._messageQueue)

    def threadedListen(self, callback=None):
        self.bindKeysToQueue([f"#.{self.user}.#", "#.broadcast.#"])
        Thread(
            target=self.startConsuming,
            args=(callback,),
            daemon=True,
        ).start()


class CommsSender(Comms):
    def __init__(self, **kwargs):
        """Extends Comms and adds a "send" method which sends data to a
        specified channel (exchange).
        """
        super().__init__(**kwargs)

    def send(self, routing_key, body, closeConnection=True):
        print(f"Sending: routing_key: {routing_key}, body: {body}")

        body = json.loads(body)

        body["from"] = self.user

        self.channel.basic_publish(
            self.exchange, routing_key=routing_key, body=json.dumps(body)
        )
        if closeConnection:
            self.connection.close()

    def threadedSend(self, routing_key, body, closeConnection=False):
        print(f"Calling send via Thread")

        Thread(
            target=self.send,
            args=(
                routing_key,
                body,
                closeConnection,
            ),
            daemon=True,
        ).start()

    def closeConnection(self):
        self.connection.close()


def usage():
    print("Error: You need to choose `send` or `listen` and optionally `teamName`!")
    print("Usage: python CommsClass <send,listen>")
    sys.exit()


players = ["player-1", "player-2"]
cmds = ["message", "broadcast", "move", "fire"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    method = sys.argv[1]

    if len(sys.argv) > 2:
        numCmds = sys.argv[2]
    else:
        numCmds = 3

    # teams = ["team-1", "team-2", "team-3", "team-4", "team-5"]

    body = {
        "message": ["hello", "whatsup", "show me the money", "god bless merica"],
        "broadcast": ["hello", "whatsup", "show me the money", "god bless merica"],
        "move": [{"x": random.randint(1, 100), "y": random.randint(1, 100)}],
        "fire": [
            {
                "x": random.randint(1, 100),
                "y": random.randint(1, 100),
                "bearing": random.choice(["N", "S", "E", "W"]),
            }
        ],
    }

    user = random.choice(players)
    target = random.choice(players)

    creds = {
        "exchange": "messages",
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": user,
        "password": "rockpaperscissorsdonkey",  # user.capitalize() * 3,
    }

    if method == "send":
        commsSender = CommsSender(**creds)
        for i in range(numCmds):
            cmd = random.choice(cmds)
            data = random.choice(body[cmd])
            commsSender.send(target, json.dumps({"cmd": cmd, "body": data}), False)
            time.sleep(2)

    else:
        print("Comms Listener starting. To exit press CTRL+C ...")
        commsListener = CommsListener(**creds)
        commsListener.bindKeysToQueue([f"#.{user}.#", "#.broadcast.#"])
        commsListener.startConsuming()
