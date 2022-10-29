import pygame, sys
from Board import Board
from Agents import Random_AI, One_Move_AI, Minimax_AI
from settings import size, p1, p2, AI_delay



# adjust settings
p1_AI = not p1 == 'Human'
p2_AI = not p2 == 'Human'
agents = []
for i in range(2):
    setting = p1 if i == 0 else p2
    if setting == 'Random':
        agents.append(Random_AI())
    elif setting == 'One Mover':
        agents.append(One_Move_AI())
    elif setting == 'Minimax':
        agents.append(Minimax_AI())
    else:
        agents.append(None)



# setup display global variables
pygame.init()
pygame.display.set_caption('Tic-Tac-Toe')
width, height = size
screen = pygame.display.set_mode(size)
image_size = (size[0]//6, size[1]//6)
x_img = pygame.transform.scale(pygame.image.load("images/X.png"), image_size)
o_img = pygame.transform.scale(pygame.image.load("images/O.png"), image_size)
font = pygame.font.Font('freesansbold.ttf', 64)
pygame.display.flip()

def make_display():
    # setup the images
    screen.fill((255, 255, 255))

    # draw in lines
    horiz_width = vert_width = min(height, width) // 50
    horiz_length = 3 * (width // 4) - int(.5*image_size[0])
    vert_length = 5 * (height // 8) + int(.25*image_size[1])
        # vertical lines
    x_1 = width//2 - (width//8)
    x_2 = width//2 + (width//8)
    top = 5*(height//8) - (height//4) - int(.5*image_size[1])
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(x_1, top, horiz_width, vert_length))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(x_2, top, horiz_width, vert_length))
        # horizontal lines
    y_1 = 5*(height//8) - (height//8)
    y_2 = 5*(height//8) + (height//8)
    left = width//2 - (width//4) - int(.5*image_size[0])
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(left, y_1, horiz_length, vert_width))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(left, y_2, horiz_length, vert_width))

    # render text
    text = font.render('Tic-Tac-Toe', True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 16)
    screen.blit(text, textRect)

    # update display
    pygame.display.flip()

def draw_image(img, row, col):
    # draw the shape in given location
    x_pos = width//2 + (col - 1)*(width//4) - int(.5*image_size[0])
    y_pos = 5*(height//8) + (row - 1 )*(height//4) - int(.5*image_size[1])
    screen.blit(img, (x_pos, y_pos))
    pygame.display.flip()

def update_display(turn):
    # cover up old text
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, height//8, width, height//8))
    # update display text
    color = (255, 0, 0) if turn == 'X' else (0, 0, 255)
    text = font.render("{}'s turn".format(turn), True, color, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (width // 2, 1.5*(height // 8))
    screen.blit(text, textRect)
    pygame.display.flip()

def calc_location():
    mouse = pygame.mouse.get_pos()
    correct_row = -1
    correct_col = -1
    for col in range(3):
        x_min = width//2 + (col - 1)*(width//4) - int(.5*image_size[0])
        x_max = x_min + image_size[0]
        if mouse[0] > x_min and mouse[0] < x_max:
            correct_col = col
            break
    for row in range(3):
        y_min = 5*(height//8) + (row - 1 )*(height//4) - int(.5*image_size[1])
        y_max = y_min + image_size[1]
        if mouse[1] > y_min and mouse[1] < y_max:
            correct_row = row
            break
    if correct_row == -1 or correct_col == -1:
        return -1, -1, -1
    translation_array = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    return correct_row, correct_col, translation_array[correct_row][correct_col]

def display_winner(winner):
    # cover up old text
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, height//8, width, height//8))
    # update display text
    color = (255, 0, 0) if winner == 'X' else ((0, 0, 255) if winner == 'O' else (0, 150, 0))
    content = "Tie" if winner == "Tie" else "{} Won".format(winner)
    text = font.render(content, True, color, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (width // 2, 1.5*(height // 8))
    screen.blit(text, textRect)
    pygame.display.flip()
    # print(content) can be added to show winner in terminal

def execute_move(board, row, col, index, turn):
    valid = board.play_move(index, turn)
    if valid:
        winner = board.check_win() # get winner
        if board.full() and winner == '_': # check for tie
            winner = "Tie"
        draw_image(x_img if turn == 'X' else o_img, row, col)
        turn = 'X' if turn != 'X' else 'O'
        return winner, turn
    else: # keep tie and same turn on invalid move
        return '_', turn
    

def game_loop():
    make_display()
    board = Board()
    turn = 'X'
    playing = True
    winner = '_'
    
    while playing and (winner == '_'):
        # display turn
        update_display(turn)
        # have AI move if in AI mode
        if (turn == 'X' and p1_AI) or (turn == 'O' and p2_AI):
            if AI_delay == 0:
                if not (p1_AI and p2_AI): # insert .1s delay if there's a real player
                    pygame.time.delay(100)
            else:
                pygame.time.delay(int(AI_delay * 1000))
            agent = agents[0] if turn == 'X' else agents[1]
            index, col, row = agent.pick_move(board, turn)
            winner, turn = execute_move(board, row, col, index, turn)
        else:
            waiting = True
            while waiting:
                # check for updates
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Determine which square was clicked
                        row, col, index = calc_location()
                        if (index != -1):
                            # Execute Move
                            winner, turn = execute_move(board, row, col, index, turn)
                            waiting = False
    display_winner(winner)
    
def control_function():
    # start by playing the game
    game_loop()
    running = True
    while running:
        # let them click to play again
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()

if __name__ == '__main__':
    control_function()
