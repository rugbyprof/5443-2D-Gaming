import pygame
import math
import sys
from comms import CommsSender, CommsListener
import json

# Initializing Pygame
pygame.init()



# Screen
WIDTH = 500
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")x

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("X.png"), (150, 150))
O_IMAGE = pygame.transform.scale(pygame.image.load("O.png"), (150, 150))

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)

game_array = []

player = None

def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)


def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y, "", True)

    return game_array


def click(game_array,m_x=None,m_y=None):
    global x_turn, o_turn, images

    # Mouse position
    if not m_x:
        m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                if x_turn:  # If it's X's turn
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = (x, y, 'x', False)

                elif o_turn:  # If it's O's turn
                    images.append((x, y, O_IMAGE))
                    x_turn = True
                    o_turn = False
                    game_array[i][j] = (x, y, 'o', False)


# Checking if someone has won
def has_won(game_array):
    # Checking rows
    for row in range(len(game_array)):
        if (game_array[row][0] == game_array[row][1] == game_array[row][2]) and game_array[row][0] != "":
            display_message(game_array[row][0].upper() + " has won!")
            return True

    # Checking columns
    for col in range(len(game_array)):
        if (game_array[0][col] == game_array[1][col] == game_array[2][col]) and game_array[0][col] != "":
            display_message(game_array[0][col].upper() + " has won!")
            return True

    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won!")
        return True

    # Checking reverse diagonal
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        display_message(game_array[0][2][2].upper() + " has won!")
        return True

    return False


def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True


def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()

def localCallBack(ch, method, properties, body):
    global game_array
    global player
    body = json.loads(body)
    # print(player)
    # print(ch)
    # print(method)
    # print(properties)
    print(body)
    click(game_array,body['m_x'],body['m_y'])



def main(player):

    global game_array, x_turn, o_turn, images, draw

    if player == 'player-1':
        target = 'player-2'
    else:
        target = 'player-1'

    game_array = initialize_grid()
    creds = {
        "exchange": "pygame2d",
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": player,
        "password": "rockpaperscissorsdonkey",
    }

    # create instances of a comms listener and sender
    # to handle message passing.
    commsListener = CommsListener(**creds)
    commsSender = CommsSender(**creds)

    # Start the comms listener to listen for incoming messages
    commsListener.threadedListen(localCallBack)


    images = []
    draw = False

    run = True

    x_turn = True
    o_turn = False

    

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array)
                m_x, m_y = pygame.mouse.get_pos()
                commsSender.threadedSend(
                    target, json.dumps({"command": "click","m_x":m_x,"m_y":m_y})
            )

        render()

        if has_won(game_array) or has_drawn(game_array):
            run = False



if __name__ == '__main__':
    print(localCallBack)
    if len(sys.argv) < 2:
        print("need player name")
        sys.exit()
    player = sys.argv[1]
    main(player)
