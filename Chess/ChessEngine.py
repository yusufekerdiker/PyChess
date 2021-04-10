'''
This class is responsible for storing all the info about current chess game status.
It will also responsible for determining valid moves at current status. It will also keep a move log.
'''

class GameState():

    def __init__(self):

        # board is 2d 8x8 size, each piece in list has 2 characters
        # first char represents the color of piece black: 'b' and white: 'w'
        # second char represents the type of piece king: 'K', Queen: 'Q', Rook: 'R', Bishop: 'B', Knight: 'N', Pawn: 'P'
        # "--" represents empty space on the chess table(an empty space with no piece)
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.whiteToMove = True
        self.moveLog = []