import os
import numpy as np
import sys
sys.path.append('..')

import argparse
from NNModel import NNModel as onnet

args = {
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': True,
    'num_channels': 512,
}

class NeuralNet():
    def __init__(self, game):
        self.nnet = onnet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_boards, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        self.nnet.model.fit(x = input_boards, y = [target_pis, target_vs], batch_size = args["batch_size"], epochs = args["epochs"])

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        # start = time.time()
        swap = board[-1][-1]
        
        if swap:
            board *= -1
        
        board = np.delete(board, self.board_x, 0) # Delete last row before predicting from NN

        # preparing input
        board = board[np.newaxis, :, :]
        
        pi, v = self.nnet.model.predict(board, verbose=False)

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # change extension
        filename = filename.split(".")[0] + ".h5"
        
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # change extension
        filename = filename.split(".")[0] + ".h5"
        
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise("No model in path {}".format(filepath))
        self.nnet.model.load_weights(filepath)
