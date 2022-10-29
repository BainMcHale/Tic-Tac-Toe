'''
The board is stored as a 9 character string of O, X, or _
Visually, the indexes correspond to these positions on the board:
1 | 2 | 3
----------
8 | 0 | 4
----------
7 | 6 | 5
'''
class Board:
    """
    Function Name: __init__
    Description: initializes board with default being empty
    Parameters: 9 character string consisting of O, X, or _
    """
    def __init__(self, board_pos = '_________', valid=None):
        # create board state
        self.data = board_pos

        # generate what moves are valid of not passed in
        if valid != None:
            self.valid = valid.copy()
        else:
            self.valid = set()
            for i in range(len(board_pos)):
                if board_pos[i] == '_':
                    self.valid.add(i)

    """
    Function Name: play_move
    Description: will add a specific move to the board
    Parameters: position is 0-8 for board location, player is X, O, or _
    Return Value: True if execute, false if invalid move
    """
    def play_move(self, position, player):
        if position in self.valid:
            self.data = self.data[:position] + player + self.data[position+1:]
            self.valid.remove(position)
            return True
        return False # do nothing if invalid move

    """
    Function Name: check_win
    Description: checks all areas to see if a player has won
    Return Value: X or O corresponding to winner, _ if no winner
    """
    def check_win(self):
        # check edges
        for i in range(1, 5):
            # pull data
            left = self.data[2*i - 1]
            middle = self.data[2*i]
            if 2*i + 1 == 9:
                right = self.data[1]
            else:
                right = self.data[2*i + 1]

            # check for match
            if left == middle == right != '_':
                return middle

        # check middle row and column
        if self.data[2] == self.data[0] == self.data[6] != '_':
                return self.data[0]
        if self.data[4] == self.data[0] == self.data[8] != '_':
                return self.data[0]

        # check diagonals
        if self.data[1] == self.data[0] == self.data[5] != '_':
                return self.data[0]
        if self.data[3] == self.data[0] == self.data[7] != '_':
                return self.data[0]

        # no winner has been found if you get here
        return '_'
    """
    Function Name: rotate
    Description: rotates the board 90° counterclockwise
    """
    def rotate(self):
        self.data = self.data[0] + self.data[3:] + self.data[1:3]

    """
    Function Name: reflect
    Description: horizontally symmetrically flip the board about the center
    """
    def reflect(self):
        self.data = self.data[0] + self.data[3:0:-1] + self.data[8] + self.data[7:4:-1] + self.data[4]

    """
    Function Name: copy
    Description: creates a copy of the board that can be played on independently
    Return Value: deep copy with new Board() object
    """
    def copy(self):
        return Board(self.data, self.valid)

    """
    Function Name: full
    Description: determines if another move can be played
    Return Value: True if board is full and cannot be played on, False if not
    """
    def full(self):
        return '_' not in self.data

    """
    Function Name: print_board
    Description: will print out the state of the Board
    """
    def print_board(self):
        print("{} | {} | {}".format(self.data[1], self.data[2], self.data[3]))
        print("__________")
        print("{} | {} | {}".format(self.data[8], self.data[0], self.data[4]))
        print("__________")
        print("{} | {} | {}".format(self.data[7], self.data[6], self.data[5]))
