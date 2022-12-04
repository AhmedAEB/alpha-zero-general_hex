class Board():
    def __init__(self, n, turn=0):
        "Set up initial board configuration."
        self.n = n
        # self.legal_moves = set()
        self.turn = turn

        # Create the empty board array.
        self.pieces = [None] * self.n
        for i in range(self.n):
            self.pieces[i] = [0] * self.n

        # Initialize the legal moves.
        # for y in range(self.n):
        #     for x in range(self.n):
        #         self.legal_moves.add((x,y))

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all empty locations.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    moves.add((x, y))
        return list(moves)

    def has_legal_moves(self):
        """Returns True if has legal move else False
        """
        # Get all empty locations.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    return True
        return False

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """
        (x, y) = move
        try:
            assert self[x][y] == 0
        except AssertionError:
            print(move, color, self.pieces)
            raise AssertionError
        self[x][y] = color
        # self.legal_moves.remove(move)
