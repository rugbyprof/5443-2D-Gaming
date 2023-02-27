"""
After we saw how to control each player using event logic,
could we use similar logic to do the same for a multiplayer game?
Instead of directly controlling each player, we could let commands 
comming from a specific player be passed to a "dot" instance to move
it. 

First however, lets get a comms example that will let players wanting
to be added to the same game get added and basically "appear" when they
send a message to the same game queue you are on. 
"""
import pygame
from random import randint
import json
import sys 
from rich import print

# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender

class Messenger:
    def __init__(self,creds,callback=None):
        self.creds = creds
        self.callBack = callback
        
        if not self.creds:
            print("Error: Message handler needs `creds` or credentials to log into rabbitmq. ")
            sys.exit()
            
        if not self.callBack:
            print("Error: Message handler needs a `callBack` function to handle responses from rabbitmq. ")
            sys.exit()
        
        
        self.user = self.creds['user']
    
        # create instances of a comms listener and sender
        # to handle message passing.
        self.commsListener = CommsListener(**self.creds)
        self.commsSender = CommsSender(**self.creds)

        # Start the comms listener to listen for incoming messages
        self.commsListener.threadedListen(self.callBack)




    def send(self,**kwargs):
        """
        """
        target = kwargs.get('target','broadcast')
        self.commsSender.threadedSend(
            target=target, sender=self.user,body =json.dumps(kwargs),debug=False
        )

class BasicPlayer:
    def __init__(self,screen):
        """_summary_

        Args:
            screen (_type_): _description_
            creds (_type_): _description_
        """
        
        self.screen = screen    # copy of screen to display dot on

        # set the initial position of the dot
        self.dot_position = pygame.math.Vector2(randint(25,400), randint(25,400))
        self.speed = 1
        self.color = (randint(0,256),randint(0,256),randint(0,256))
        self.ticks = 0


    def update(self,keys):
        """ Get the keys from main, then adjust position based
            on keys pressed
        """
        if keys[pygame.K_UP]:
            self.dot_position.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.dot_position.y += self.speed
        if keys[pygame.K_LEFT]:
            self.dot_position.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.dot_position.x += self.speed


    def draw(self):
        # draw the dot
        pygame.draw.circle(self.screen, self.color , self.dot_position, 10)



class Player(BasicPlayer):
    def __init__(self,screen,creds,callback=None):
        """_summary_

        Args:
            screen (_type_): _description_
            creds (_type_): _description_
        """
        
        super().__init__(screen)
        self.creds = creds
        self.id = self.creds['user'] 
        

        self.messenger = Messenger(self.creds,callback)

        
    def broadcastLocation(self):
        # only send a message so many ticks otherwise problems occur!
        #print(pygame.time.get_ticks() - self.ticks)
        if pygame.time.get_ticks() - self.ticks > 100:
            pos = (self.dot_position.x,self.dot_position.y)
            self.messenger.send(
                target='broadcast', sender=self.id, player=self.id,dot_position=pos
            )
            self.ticks = pygame.time.get_ticks()

    def draw(self):
        self.broadcastLocation()
        # draw the dot
        pygame.draw.circle(self.screen, self.color , self.dot_position, 10)




class GameManager:
    def __init__(self,screen):
        self.players = {}
        self.screen = screen
        self.localPlayer = None

    def addPlayer(self,player,local=False):
        if not player.id in self.players:
            self.players[player.id] = player
        
        if local:
            self.localPlayer = self.players[player.id]

    def draw(self):
        for id,player in self.players.items():
            if not id == self.localPlayer:
                player.draw()

    def callBack(self, ch, method, properties, body):
        """_summary_: callback for multiple players

        Args:
            ch (_type_): _description_
            method (_type_): _description_
            properties (_type_): _description_
            body (_type_): _description_

        Returns:
            dictionary: results of callback
        """
        results = {}
        results['game'] = method.exchange
        results['exchange'] = method.exchange
        body = json.loads(body.decode('utf-8'))
        for k,v in body.items():
            results[k] = v

        if not results['sender'] in self.players:
            self.players[results['sender']] = BasicPlayer(self.screen)
            print(len(self.players))
        else:
            self.players[results['sender']].dot_position.x = results['dot_position'][0]
            self.players[results['sender']].dot_position.y = results['dot_position'][1]

        #print(results)
        return results

############################################################
# GLOBALS
############################################################
    
# initialize Pygame
pygame.init()

# set the window size
size = (400, 400)

# create the window
screen = pygame.display.set_mode(size)
############################################################


def main(creds):

    manager = GameManager(screen)

    localPlayer = Player(screen,creds,manager.callBack)
    
    manager.addPlayer(localPlayer,True)
   

    # set the window title
    pygame.display.set_caption(f"{creds['user']}")

    # create list for lookup for keys 0-9
    # The keys 0-9 are ascii 48-57 
    numericKeys = [x for x in range(0,58)]

    # run the game loop
    running = True
    while running:
        
        # clear the screen
        screen.fill((255, 255, 255))

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # get the keys 0-9 if pressed
                elif event.key in numericKeys:
                    print(f"You pressed: {48-event.key}")
                    # choose current dot by which key pressed
                    currentPlayer = 48 - event.key

        # move the dot based on key input
        keys = pygame.key.get_pressed()
        localPlayer.update(keys)

        manager.draw()
        
        # update the screen
        pygame.display.flip()

    # quit Pygame
    pygame.quit()

if __name__=='__main__':
    if len(sys.argv) < 4:
        print("Need: exchange playerName passWord")
        sys.exit()
    exchange = sys.argv[1]
    playerName = sys.argv[2]
    playerPass = sys.argv[3]
    creds = {
        "exchange": exchange,
        "port": '5672',
        "host": 'terrywgriffin.com',
        "user": playerName,
        "password": playerPass
    }

    main(creds)
