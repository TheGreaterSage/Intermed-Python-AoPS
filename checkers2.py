from tkinter import *
 
class CheckerSquare(Canvas):
    '''displays a square in Checkers'''
 
    def __init__(self,master,row,column,bgcolor):
        '''CheckerSquare(master,row,column)
        creates a new blank Checker square at coordinate (row,column)'''
        # create and place the widget
        Canvas.__init__(self,master,width=50,height=50,bg=bgcolor, \
                        highlightthickness=2,highlightbackground=bgcolor)
        self.grid(row=row,column=column)
        # attributes
        self.position = (row,column)
        self.bgcolor = bgcolor
        self.isKing = False
        self.hasChecker = False  # placeholders
        self.checkerColor = ''
        # bind button click to placing a piece
        self.bind('<Button-1>',master.get_click)
 
    def get_position(self):
        '''CheckerSquare.get_position() -> (int,int)
        returns (row,column) coordinate of square'''
        return self.position
 
    def draw_checker(self,color):
        '''CheckerSquare.draw_checker(color)
        changes the square so that there is a checker piece on it
        color is color of the checker'''
        self.create_oval(10,10,44,44,fill=color)  # draw the checker
        self.hasChecker = True
        self.checkerColor = color
        if self.isKing:
            self.create_text(26,36,font=('Arial',28),text='*')
 
    def delete_checker(self):
        '''CheckerSquare.delete_checker()
        changes the square so that there is no checker piece on it'''
        ovalList = self.find_all()  # find the checker
        for oval in ovalList:
            self.delete(oval)  # delete the checker
 
    def highlight(self):
        '''CheckerSquare.highlight(self)
        creates a black border around the square to indicate that
        it has been clicked and selected'''
        # set highlight background to black
        self['highlightbackground'] = 'black'
 
    def unhighlight(self):
        '''CheckerSquare.unhighlight(self)
        deletes the black border around the square to indicate that
        it has been deselected and unclicked'''
        # delete the black border by setting it to the square's color
        self['highlightbackground'] = self.bgcolor
 
    def draw_king(self):
        '''CheckerSquare.draw_king()
        changes the checker on the square so that it is a king'''
        self.isKing = True
        self.create_text(26,36,font=('Arial',28),text='*')
 
    def check_king(self):
        '''CheckerSquare.check_king()
        turns checker into a king if it should be one'''
        if self.hasChecker:  # if there is a checker on the square
            if self.checkerColor == 'red':  # if the checker is red...
                if self.position[0] == 7:  # ...and it has reached the other side...
                    self.isKing = True  # ...make it a king!
                    self.draw_king()
            elif self.checkerColor == 'white':  # same thing for white
                if self.position[0] == 0:
                    self.isKing = True
                    self.draw_king()
 
 
class CheckerBoard:
    '''represents a board of Checkers; controls the rules and directs CheckerGame'''
 
    def __init__(self):
        '''CheckerBoard()
        creates a CheckerBoard in starting position'''
        self.board = {}  # dict to store position
        # create opening position
        for row in range(8):
            for column in range(8):
                coords = (row,column)  # (row,column) tuple coordinate
                if coords in [(0,1),(0,3),(0,5),(0,7),(1,0),(1,2),(1,4),\
                              (1,6),(2,1),(2,3),(2,5),(2,7)]:
                    self.board[coords] = 0  # player 0 (red)
                elif coords in [(5,0),(5,2),(5,4),(5,6),(6,1),(6,3),(6,5),\
                                (6,7),(7,0),(7,2),(7,4),(7,6)]:
                    self.board[coords] = 1  # player 1 (white)
                else:
                    self.board[coords] = None  # no player
        self.currentPlayer = 0  # player 0 (red) starts
        self.endgame = None  # replace with a string when game ends
        self.validMove = False  # placeholder
        self.jumpMove = False # not a jump move
        self.continuingJump = False
 
    def get_piece(self,coords):
        '''CheckerBoard.get_piece(coords) -> int
        returns the piece at coords: 0, 1, or None'''
        return self.board[coords]
 
    def get_endgame(self):
        '''CheckerBoard.get_endgame()
        returns endgame state'''
        return self.endgame
 
    def get_player(self):
        '''CheckerBoard.get_player() -> int
        returns the current player'''
        return self.currentPlayer
 
    def next_player(self):
        '''CheckerBoard.next_player()
        advances to next player'''
        self.currentPlayer = 1 - self.currentPlayer
 
    def possible_moves(self,square,squareIsKing):
        '''CheckerBoard.possible_moves(): square -> tuple; squareIsKing -> bool
        Find all possible moves (as a coordinate list) and return them'''
        squareRow = square[0]
        squareColumn = square[1]
 
        options = []
        jumpOptions = []
 
        if self.continuingJump:
            return self.get_continue_jump()
 
        elif squareIsKing:
            # doesn't matter what color, if the checker is the center of this X then the edges of the X are the possible checkers assuming they're within bounds
            allOptions = [((squareRow-1),(squareColumn-1)),((squareRow-1),(squareColumn+1)),((squareRow+1),(squareColumn-1)),((squareRow+1),(squareColumn+1))]
        else:
            if self.currentPlayer == 1: # white
                toAdd = -1
            else:
                toAdd = 1
            allOptions = [((squareRow + toAdd),(squareColumn - 1)),((squareRow + toAdd),(squareColumn + 1))]
 
        # delete any options off the board
        for row in range(8):
            for col in range(8):
                for option in allOptions:
                    if option == (row,col): # valid option
                        options.append(option)
 
        # any 'options' with checker and checker color = original square color
        optionsCopy = options[:]
 
        for option in optionsCopy:
            if self.board[option] == self.board[square]:
                # remove from options
                options.remove(option)
 
        optionsCopy = options[:]
        # Now figure out if any of them have checkers of the opposite color; if so, see if you can jump over them
        for option in optionsCopy:
            if self.board[option] == 1 - self.currentPlayer: # meaning there's a checker of opposite color
                row = option[0]
                col = option[1]
 
                if squareIsKing:
                    # figure out which of the four
                    if row + 1 == squareRow:
                        rowAdd = -1
                    else:
                        rowAdd = 1
 
                    if col + 1 == squareColumn:
                        colAdd = -1
                    else:
                        colAdd = 1
 
                    # now make the new option
                    newOption = (row + rowAdd,col + colAdd)
                else:
                    # figure out which option
                    if col + 1 == squareColumn: # left option
                        columnAdd = -1
                    else:
                        columnAdd = 1
 
                    newOption = ((row + toAdd),(col+columnAdd))
 
                options.remove(option)
                if newOption in self.board and self.board[newOption] == None: # can be jumped to
                    jumpOptions.append(newOption)
 
        return [options,jumpOptions]                
 
    def try_move(self,oldSquare,newSquare,checkerIsKing):
        '''CheckerBoard.try_move(coords)
        moves the checker piece to the given square if the move is legal
        also deletes checkers if applicable and goes on to next player
        oldSquare, newSquare -> tuples
        checkerIsKing -> bool'''
        self.oldSquareCoords = oldSquare
        self.newSquareCoords = newSquare
 
        self.validMove = False  # resets to False each time
        moves = self.possible_moves(self.oldSquareCoords,checkerIsKing)
        regularOptions = moves[0]
 
        if self.continuingJump:  # if there is a continuing jump going on...
            jumpOptions = moves  # ...then the jump option is from get_continue_jump()
            self.continuingJump = False  # reset to False
        else:
            jumpOptions = moves[1]  # otherwise jump options are normal
 
        # if move is a valid move (either it is a normal move and there are no jumps available, or it is a jump):
        if self.newSquareCoords in regularOptions and jumpOptions == [] or self.newSquareCoords in jumpOptions:
            self.validMove = True
            # record the fact that the square has a checker now (will be drawn later)
            self.board[self.newSquareCoords] = self.currentPlayer
            # record the fact that the old square no longer has a checker now
            self.board[self.oldSquareCoords] = None
            self.next_player()
 
        if self.newSquareCoords in jumpOptions: # if move is a jump
            # delete the checker that is jumped
            # average of coordinates is the jumped checker
            rowCoord = (self.oldSquareCoords[0] + self.newSquareCoords[0])/2
            colCoord = (self.oldSquareCoords[1] + self.newSquareCoords[1])/2
            self.jumpMove = True
            rowCoord = int(rowCoord)
            colCoord = int(colCoord)
            self.jumpedCoord = (rowCoord,colCoord)
            # also want to update display: because self.board[self.jumpedCoord] now has nothing
            self.board[self.jumpedCoord] = None
 
            # check to see if another jump is possible
            self.next_player()
            continueJump = self.possible_moves(self.newSquareCoords,False)  # find possible moves from the square just moved to
            if continueJump[1] != []:  # if there are possible jump moves...
                self.continuingJump = True
                self.set_continue_jump(continueJump[1][0]) # ...set the continue jump options to the new square
            else:
                self.next_player()
 
 
    def set_continue_jump(self,coords):
        '''CheckerBoard.set_continue_jump(coords)
        sets the possibilities for continuing a jump to coords'''
        self.continueJumpCoords = coords
 
    def get_continue_jump(self):
        '''CheckerBoard.get_continue_jump()
        returns the possibilities for a continued jump if applicable'''
        return [self.continueJumpCoords]  # if there is a continuing jump going on, return the coordinates
 
    def valid_move(self):
        '''CheckerBoard.move_was_valid()
        checks to see if the move was valid'''
        return self.validMove
 
    def check_endgame(self):
        '''CheckerBoard.check_endgame()
        checks to see if the game is over'''
        # check_endgame is always right after someone moves, right? So we'd only need to check if the current player wins.
        playerNumber = self.currentPlayer
        possibleWinner = 1 - playerNumber
        won = True
 
        for square in self.board:
            if self.board[square] == self.currentPlayer: # if there's a checker of the opposite color
                won = False
                break # no need to continue
 
        if won:
            self.endgame = True
 
 
    def reset_jump(self):
        '''Resets the jumpMove coord to False since the jump has been dealed with already'''
        self.jumpMove = False
 
 
class CheckerGame(Frame):
    '''represents a game of Checkers; represents the user interface'''
 
    def __init__(self,master):
        '''CheckerGame(master)
        creates a new Checkers game'''
        # initialize the Frame
        Frame.__init__(self,master,bg='gray94')
        self.grid()
 
        # set up game data
        self.colors = ('red','white')  # players' colors
 
        # create board in starting position, player 0 (red) going first
        self.board = CheckerBoard()
        self.squares = {}  # stores CheckerSquares
 
        # create checker squares
        for row in range(8):
            for column in range(8):
                coord = (row,column)
                if coord in [(0,1),(0,3),(0,5),(0,7),(1,0),(1,2),(1,4),\
                              (1,6),(2,1),(2,3),(2,5),(2,7),(3,0),(3,2),\
                              (3,4),(3,6),(4,1),(4,3),(4,5),(4,7),(5,0),\
                              (5,2),(5,4),(5,6),(6,1),(6,3),(6,5),(6,7),\
                              (7,0),(7,2),(7,4),(7,6)]:
                    self.bgcolor = 'dark green'
                else:
                    self.bgcolor = 'blanched almond'
                self.squares[coord] = CheckerSquare(self,row,column,\
                                                    self.bgcolor)
 
        # set up turn indicator
        self.rowconfigure(8)
        self.turnIndicator = CheckerSquare(self,8,2,'gray94')
        self.turnIndicator.draw_checker(self.colors[0])  # player 0 (red) starts
        self.turnIndicator.unbind('<Button-1>')  # should not repond to clicks
 
        # nothing is clicked... yet
        self.pieceIsClicked = False
        self.coordsOfPieceClicked = ''
 
        # set up info label (for instructions such as 'must continue jump')
        self.infoLabel = Label(master,text='',font=('Arial',12))
        self.infoLabel.grid(row=8,column=4)
 
        # update the display
        self.update_display()
 
    def get_click(self,event):
        '''CheckerGame.get_click(event)
        event handler for mouse click
        gets click data and tries to make the move'''
        coords = event.widget.get_position()  # coords is coordinates clicked
 
        if self.squares[coords]['bg']=='blanched almond':
            # if the square is blanched almond, do nothing
            return
 
        if self.board.get_piece(coords) == None and not self.pieceIsClicked:
            # if there is no piece there and it is the first click, do nothing
            return
 
        if self.board.get_piece(coords) != self.board.currentPlayer and not self.pieceIsClicked:
            # if the square does not have the correct player's checker and it's the first click...
            return  # ...do nothing
 
        if self.pieceIsClicked:  # a piece has already been clicked
 
            if self.coordsOfPieceClicked == coords:  # same piece is clicked again
                self.squares[coords].unhighlight()  # unhighlight the piece
                self.pieceIsClicked = False  # update variables
                self.coordsOfPieceClicked = ''
 
            else: # different piece is clicked
                king = False
                if self.squares[self.coordsOfPieceClicked].isKing:
                    king = True
                    self.squares[coords].draw_king()  # make it a king
                self.board.try_move(self.coordsOfPieceClicked,coords,king)  # try the move
 
                if self.board.valid_move():  # if the move was valid
                    self.squares[coords].highlight()  # highlight the new square
                    self.squares[self.coordsOfPieceClicked].unhighlight()  # unhighlight the old square
                    self.squares[self.coordsOfPieceClicked].delete_checker()  # and delete its checker
                    if self.board.currentPlayer == 0: # red
                        color = 'white' # opposite color since in try_move, we moved to the next player
                    else: # white
                        color = 'red'
                    self.squares[coords].draw_checker(color)   # draw the new checker
                    self.pieceIsClicked = False  # even though a piece is highlighted, the move is over
                    self.coordsOfPieceClicked = ''
                    # and
                    if self.board.jumpMove: # something has been jumped so we should delete its checker
                        self.squares[self.board.jumpedCoord].delete_checker()
 
                        # then reset jumpMove
                        self.board.reset_jump()
 
                self.board.check_endgame()
 
        else:  # nothing has been clicked yet OR something has been clicked but the move is done
            for square in self.squares:
                self.squares[square].unhighlight()  # unhighlight all other pieces
            self.squares[coords].highlight()  # highlight the piece
            self.pieceIsClicked = True  # update variables
            self.coordsOfPieceClicked = coords
 
        self.update_display()  # update the display
 
    def update_display(self):
        '''CheckerGame.update_display()
        updates squares to match board
        updates turn label and info label'''
        # update squares
        for row in range(8):
            for column in range(8):
                coord = (row,column)
                piece = self.board.get_piece(coord)
                if not self.squares[coord].isKing:
                    self.squares[coord].check_king()  # check all squares to see if they are kings
                if piece is not None:
                    self.squares[coord].draw_checker(self.colors[piece])  # draw the board in updated position
        # update turn indicator
        self.turnIndicator.draw_checker(self.colors[self.board.get_player()])
 
        # check to see if game is over
        endgame = self.board.get_endgame()
        if endgame is not None:  # game is over
            # remove the turn indicator
            self.turnIndicator.delete_checker()
            # print a message indicating who won
            if self.board.currentPlayer == 0: # red's turn meaning white won
                winner = 'white'
            else:
                winner = 'red'
            self.infoLabel['text']=('Player ' + winner + ' won!')
 
 
def play_checkers():
    '''play_checkers()
    starts a new game of Checkers'''
    root = Tk()
    root.title('Checkers')
    cg = CheckerGame(root)
    cg.mainloop()
 
play_checkers()
