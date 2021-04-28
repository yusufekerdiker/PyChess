"""
This is main driver file.
It will responsible for handling user input choice and display the moves/GameState object
"""

import pygame as p
from PyChess.Chess import ChessEngine

WIDTH = HEIGHT = 512    # max hi-res
DIMENSION = 8   # size of chessboard 8x8
SQ_SIZE = HEIGHT // DIMENSION   # square size and 512 iz power of 2 -- 2^9
MAX_FPS = 144   # for animation smoothness, based on my monitor i am choosing 144fps/144hz
IMAGES = {}

"""
pictures need to upload and used only one for saving resource(like lazy singleton)
Initialize a global dic of images. This will be called exactly once in the main
"""

def loadImages():

    pieces = ['wR', 'wN', 'wB', 'wK', 'wQ', 'wp', 'bR', 'bN', 'bB', 'bK', 'bQ', 'bp']

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    # note: we can access an image by saying 'IMAGES['wP']' simpler

"""
here is main drive for the code. this will handle user input and updating graphics
"""
def main():

    p.init()

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    screen.fill(p.Color("white"))

    gs = ChessEngine.GameState()    # call constructor
    #print(gs.board)

    loadImages()    # only do once, before while loop

    running = True
    sqSelected = () # no square selected, keep track the last click of the user (tuple: (row, col))
    playerClicks = [] # keep track of player clicks (two tuples: [ (6, 4), (4, 4)] )
    while running:

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:

                location = p.mouse.get_pos() # (x, y) location of mouse
                col = location[0]//SQ_SIZE #x
                row = location[1]//SQ_SIZE #y

                if sqSelected == (row, col): # the user clicked the same square twice
                    sqSelected = () # deselect
                    playerClicks = [] # clear player click

                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both 1st and second clicks

                # ask was that the users 2nd click? and if it is do:
                if len(playerClicks) == 2: # after the second click
                    # player picked second square engine move the piece
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () # reset user clicks
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
responsible for all visual within current game status
"""
def drawGameState(screen, gs):

    drawBoard(screen)     # draw square on the board
    # add in piece highlighting or move suggestions (do later)
    drawPieces(screen, gs.board)     # draw pieces  on top of those quarters

"""
draw the squares on the board. (do later: user color pick)
top left always light color
"""
def drawBoard(screen):  # call board first so pieces wont stuck under the board

    colors = [p.Color(255, 255, 255), p.Color(150, 150, 150)] # pick any color you want
    # write a color name as "white" or "gray" or write rgb values as 255, 255, 255 or 54, 38, 36

    for r in range(DIMENSION): #row

        for c in range(DIMENSION): #column
            color = colors[ ((r+c)%2) ] #gives odd or even number at end of mod
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):

    for r in range(DIMENSION): #row

        for c in range(DIMENSION): #column
            piece = board[r][c]

            if piece != "--": # non empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()