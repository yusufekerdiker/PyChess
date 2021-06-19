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

        self.moveFunctions = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }

        self.whiteToMove = True
        self.moveLog = []

    """
    takes a move as a parameter and executes it (wont work for castling, pawn promotion and en-passant)
    """

    def makeMove(self, move):

        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap player no longer white's turn

    """
    undo the last move made
    """

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back

    """
    all moves considering checks
    """

    def getValidMoves(self):
        return self.getAllPossibleMoves()  # for now no need to worry about checks

    """
    all moves without considering checks
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # num of row
            for c in range(len(self.board[r])):  # get num of cols in given row which is r
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # calls the appropriate move function based on piece type (like switch-case)
                    """
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    if piece == 'R':
                        self.getRookMoves(r, c, moves)
                    """
        return moves

    """
    get all the pawn moves for the pawn located at row, col and add these moves to the list
    """

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn's move
            if self.board[r - 1][c] == "--":  # 1 square pawn advance check
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance check / white pawn
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # capture to the left
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to the right
                if self.board[r - 1][c + 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

    """
    get all the rook moves for the rook located at row, col and add these moves to the list
    """

    def getRookMoves(self, r, c, moves):
        pass

    """
    get all the knight moves for the knight located at row, col and add these moves to the list
    """

    def getKnightMoves(self, r, c, moves):
        pass

    """
    get all the bishop moves for the bishop located at row, col and add these moves to the list
    """

    def getBishopMoves(self, r, c, moves):
        pass

    """
    get all the queen moves for the queen located at row, col and add these moves to the list
    """

    def getQueenMoves(self, r, c, moves):
        pass

    """
    get all the king moves for the king located at row, col and add these moves to the list
    """

    def getKingMoves(self, r, c, moves):
        pass


class Move():
    # maps keys to values
    # key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}  # for reversing the dict on above

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}  # for reversing the dict on above

    def __init__(self, startSq, endSq, board):  # make sure pieces are making valid moves

        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    """
    @Override the equals method (java)
    """

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
