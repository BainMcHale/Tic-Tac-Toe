from Board import Board
import random

class Random_AI:
    def __init__(self):
        pass

    def pick_move(self, board, turn):
        board_data = board.data
        valid_set = board.valid
        index = random.sample(list(valid_set), 1)[0]
        translate_table = [(1, 1), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
        row, col = translate_table[index]
        return index, col, row

class One_Move_AI:
    def __init__(self):
        pass
        
    def pick_move(self, board, turn):
        board_data = board.data
        valid_set = board.valid
        # check if it can win
        best_move = None
        for index in valid_set:
            board = Board(board_data)
            board.play_move(index, turn)
            winner = board.check_win()
            if winner == turn:
                best_move = index
                break

        # If not, stop opponent from winning by blocking
        opp_turn = 'X' if turn != 'X' else 'O'
        if best_move == None:
            for index in valid_set:
                board = Board(board_data)
                board.play_move(index, opp_turn)
                winner = board.check_win()
                if winner == opp_turn:
                    best_move = index
                    break

            # if no blocks or wins, pick randomly
            if best_move == None:
                best_move = random.sample(list(valid_set), 1)[0]
        
        translate_table = [(1, 1), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
        row, col = translate_table[best_move]
        return best_move, col, row

"""
Function Name: minimax_helper
Description: recursive function that perferms minimax from a given position
             values—  X wins: 1, Tie: 0, O wins: -1
Return Value: 2 arg tuple of (best_moves, value)
"""
def minimax_helper(agent, board, turn, alpha, beta):
    best_value = -2 if turn == 'X' else 2 # start with impossibly bad values
    best_moves = []
    for move in board.valid:
        # simulate move on new board
        new_board = board.copy()
        new_board.play_move(move, turn)
        # try to pull data from cache
        if new_board.data in agent.seen_cache:
            value = agent.seen_cache[new_board.data]
        else: # finish expansion if it's a new node
            # update node expansion count
            agent.num_nodes += 1
            
            # finish this check
            winner = new_board.check_win()

            # assign value (recurse if undecided)
            if winner == '_' and not new_board.full():
                value = minimax_helper(agent, new_board, 'X' if turn != 'X' else 'O', alpha, beta)[1]
            else:
                value = 0 if winner == '_' else (1 if winner == 'X' else -1)

            # add all permutations of reflection and rotate
            for _ in range(2):
                new_board.reflect()
                for _ in range(4):
                    new_board.rotate()
                    agent.seen_cache[new_board.data] = value
        
        # if better value, pick it
        if value == best_value:
            best_moves.append(move)
        elif turn == 'X' and value > best_value:
            best_value = value
            best_moves = [move]        
        elif turn == 'O' and value < best_value:
            best_value = value
            best_moves = [move]

        # do pruning
        if agent.pruning:
            if turn == 'X':
                alpha = max(alpha, value)
            elif turn == 'O':
                beta = min(beta, value)
            if beta < alpha:
                break
    return best_moves, best_value
        


class Minimax_AI:
    def __init__(self, pruning=True, show_report=False):
        self.num_nodes = 0
        self.seen_cache = {}
        self.show_report = show_report # turn on to see how many nodes were checked
        self.pruning=pruning # implements alpha-beta pruning

    def pick_move(self, board, turn):
        self.num_nodes = 0
        self.seen_cache = {}
        moves, value = minimax_helper(self, board, turn, -2, 2)
        if self.show_report:
            print("\n{} Nodes Checked".format(self.num_nodes))
            print(value)
            if abs(value) == 1:
                print("\nAI has won\n")
            else:
                print("still a tie")
        move = random.sample(moves, 1)[0]
        translate_table = [(1, 1), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
        row, col = translate_table[move]
        return move, col, row
    
