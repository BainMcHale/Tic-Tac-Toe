# Tic-Tac-Toe
A Tic Toe Toe play environment with AI agents to play against

## Starting a Game
To start a game type "python app.py" in the command line. After finishing a game, clicking the screen will start a new one.
X's always go first and O's always go second.

## AI agents
There are 3 agents eligible to play against. Code for them is in Agents.py.
### Random_AI
This AI simply picks a random valid move

### One_Move_AI
This agent will see if it can win on its move or block a win coming next move, but it only checks one move deep.
Otherwise, it will play randomly.

### Minimax_AI
This agent implements the minimax algorithm with no maximum depth. It will exhaustively search the tree for a winning path.
If no winning path is found, it will choose randomly from the tied paths.

## Settings
edit the settings.py file to adjust the game. This allows customization of screen size, AI agent behavior.
### Variables
##### size
give the width and height of play screen as a 2 argument tuple (width, height)
##### p1/p2
Enter who is playing as p1 and p2 as a string. Options are:
    Human
    Random
    One Mover
    Minimax
##### AI_Delay
Seconds of delay between AI moves. Useful if you want to watch the game.
