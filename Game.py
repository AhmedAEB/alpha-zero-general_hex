from __future__ import print_function
import sys
sys.path.append('..')
from Board import Board
import numpy as np

I_DISPLACEMENTS = [-1, -1, 0, 1, 1, 0]
J_DISPLACEMENTS = [0, 1, 1, 0, -1, -1]

class Game():
    def __init__(self, n=15, is_mcts=False  ):# , nir=5):
        self.n = n
        self.turns = 0
        # self.n_in_row = nir

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions 
        return self.n * self.n + 1 #(for swap)

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n * self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    # modified
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        if len(legalMoves) == 0 or self.turns == 1:
            valids[-1] = 1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        return np.array(valids)

    def DFS(self, board, player, x, y, visited):
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            return False
        if board[x][y] != player:
            return False
        if visited[x][y]:
            return False
        visited[x][y] = True
        if (player == 1 and x == self.n - 1) or (player == -1 and y == self.n - 1):
            return True
        return any(self.DFS(board, player, x + I_DISPLACEMENTS[i], y + J_DISPLACEMENTS[i], visited) for i in range(6))

    # modified
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        # n = self.n_in_row

        # Check if player 1 has a winning path from top to bottom
        for i in range(self.n):
            if self.DFS(board, 1, 0, i, [[False] * self.n for _ in range(self.n)]):
                return 1
                
        # Check if player 2 has a winning path from left to right
        for i in range(self.n):
            if self.DFS(board, -1, i, 0, [[False] * self.n for _ in range(self.n)]):
                return -1

        if b.has_legal_moves():
            return 0
        return 1e-4
    

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return board.copy() # Rules for hex are different (inverting results in false wins)

    # modified
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []
    
        l += [(board, pi)]
        l += [(np.fliplr(board), list(np.fliplr(pi_board).ravel()) + [pi[-1]])]
        l += [(np.flipud(board), list(np.flipud(pi_board).ravel()) + [pi[-1]])]
        l += [(np.flipud(np.fliplr(board)), list(np.flipud(np.fliplr(pi_board)).ravel()) + [pi[-1]])]
    
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    @staticmethod
    def display(board):
        n = board.shape[0]

        for y in range(n):
            print(y, "|", end="")
        print("")
        print(" -----------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                if piece == -1:
                    print("B ", end="")
                elif piece == 1:
                    print("R ", end="")
                else:
                    if x == n:
                        print("-", end="")
                    else:
                        print("- ", end="")
            print("|")
        print("   -----------------------")

if __name__=="__main__":
    g = Game(11)
    n = 11
    x = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, -1, -1, -1, 0, 0],
                  [0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
                  [-1, -1, 0, 0, -1, 0, 0, 0, -1, 0, 1],
                  [0, -1, 0, -1, 0, 0, 0, 0, -1, -1, 1],
                  [0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    b = Board(11)
    b = np.array(b.pieces)

    pi = [0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.0, 0.041666666666666664, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.041666666666666664, 0.0, 0.041666666666666664, 0.0, 0.0, 0.0, 0.041666666666666664, 0.041666666666666664, 0.041666666666666664, 0.0, 0.041666666666666664, 0.041666666666666664, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.041666666666666664, 0.0, 0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.0, 0.041666666666666664, 0.041666666666666664, 0.041666666666666664, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.041666666666666664, 0.041666666666666664, 0.0, 0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.041666666666666664, 0.0, 0.0, 0.0]
    pi_board = np.reshape(pi[:-1], (11, 11))

    l = []

    l = [(b, pi)]

    l_90 = [(np.fliplr(b), list(np.fliplr(pi_board).ravel()) + [pi[-1]])]

    l_180 = [(np.fliplr(np.fliplr(b)), list(np.fliplr(np.fliplr(pi_board)).ravel()) + [pi[-1]])]

    l_270 = [(np.fliplr(np.fliplr(np.fliplr(b))), list(np.fliplr(np.fliplr(np.fliplr(pi_board))).ravel()) + [pi[-1]])]

    l_360 = [(np.fliplr(np.fliplr(np.fliplr(np.fliplr(b)))), list(np.fliplr(np.fliplr(np.fliplr(np.fliplr(pi_board)))).ravel()) + [pi[-1]])]



    print(l_180)
    # l += [(np.flipud(b), list(np.flipud(pi_board).ravel()) + [pi[-1]])]
    # l += [(np.flipud(np.fliplr(b)), list(np.flipud(np.fliplr(pi_board)).ravel()) + [pi[-1]])]



    # Outputs 0



