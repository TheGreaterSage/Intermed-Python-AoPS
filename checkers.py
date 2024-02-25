from tkinter import *
from tkinter import messagebox

class CheckerSquare(Canvas):
    def __init__(self, master, coords):
        '''CheckerSquare.__init__(master, coords) -> CheckerSquare object
        initializes the CheckerSquare object'''
        Canvas.__init__(self, master, width=50, height=50, bg = 'blanched almond', highlightthickness=2) #initialize Canvas
        self.grid(row=coords[0], column=coords[1]) 
        if (coords[0] + coords[1]) % 2 == 1:
            self['bg'] = 'dark green' 
        #set variables
        self.coords = coords
        self.empty = True
        self.bind('<Button-1>', self.clicked)
        self.selected = False
        self.master = master
        self.color = None
        self.king = False

    def get_coords(self):
        '''CheckerSquare.get_coords() -> tuple
        returns the coordinates of this square on the board'''
        return self.coords

    def get_color(self):
        '''CheckerSquare.get_color() -> str
        returns the color of the checker
        the color is None if there is no checker on the square
        the color is the color of the checker if there is a checker'''
        return self.color

    def is_empty(self):
        '''CheckerSquare.is_empty() -> bool
        returns True if the square is empty
        returns False if the square has a checker object on it'''
        return self.empty

    def is_selected(self):
        '''CheckerSquare.get_color() -> bool
        returns whether the square is selected or not'''
        return self.selected

    def is_king(self):
        '''CheckerSquare.is_king()
        returns whether the square has a king piece or not'''
        return self.king

    def place_checker(self, color):
        '''CheckerSquare.place_checker(color)
        places a checker in the CheckerSquare of the specified color
        if the square is a king, place a king piece'''
        self.create_oval(10, 10, 44, 44, fill = color)
        self.color = color
        self.empty = False
        if self.king:
            self.create_text(28, 32, text="*", font=("Arial", 20, 'bold'))

    def set_king(self):
        '''CheckerSquare.set_king()
        sets the square as king to True'''
        self.king = True

    def clear(self):
        '''CheckerSquare.clear()
        clears all items from the CheckerSquare and resets some data'''
        widgetList = self.find_all()
        for widget in widgetList:
            self.delete(widget)
        self.empty = True
        self.color = None

    def select(self, color):
        '''CheckerSquare.select(color)
        highlights the CheckerSquare with the specified color'''
        self['highlightbackground'] = color
        self.selected = True

    def unselect(self):
        '''CheckerSquare.unselect()
        resets the highlight background of the CheckerSquare'''
        self['highlightbackground'] = 'lightgray'
        self.selected = False

    def clicked(self, event):
        '''CheckerSquare.clicked(event)
        handles clicks on CheckerSquare objects
        click the first square to select it
        click the second one to attempt to move a checker from the first square to the second square
        handles kings too'''
        #if selecting own piece
        if not self.empty and self.color == self.master.turn:
            if not self.selected:
                if not self.master.selected():
                    self.select('black')
                    self.master.checker = self

            else:
                self.master.unselect_all()
        
        elif self.empty:
            #if already selected
            if self.master.selected():
                self.master.target = self                    
                if self.master.is_valid_move(self.master.checker, self.master.target) == 'forward':
                    self.master.move_checker(self.master.checker, self.master.target)
                    self.master.unselect_all()
                    self.master.take_turn()
                elif self.master.is_valid_move(self.master.checker, self.master.target) == 'jump':
                    jumped_checker = self.master.squares[((self.master.checker.get_coords()[0] +
                    self.master.target.get_coords()[0])/2, (self.master.checker.get_coords()[1] + self.master.target.get_coords()[1])/2)]
                    self.master.move_checker(self.master.checker, self.master.target)
                    jumped_checker.clear()
                    if jumped_checker.is_king():
                        jumped_checker.king = False
                    self.master.unselect_all()
                    if self.master.valid_jump(self.master.target) > 0:
                        self.master.checker = self.master.target
                        self.master.target = None
                        self.master.checker.select('black')
                        self.master.infoLabel.grid(row=8, column=3, columnspan=5)
                        self.master.infoLabel['text'] = "Must continue jump!"
                        
                    else:
                        self.master.take_turn()
                else:
                    self.master.unselect_all()
                    
class CheckerBoard(Frame):
    def __init__(self, master):
        '''CheckerBoard.__init__(self, master) -> CheckerBoard object
        initializes the Checker Board'''
        #initialize frame
        Frame.__init__(self, master, bg = "white")
        #dict for squares
        self.grid()
        self.squares = {}
        for row in range(8):
            for col in range(8):
                self.squares[(row, col)] = CheckerSquare(self, (row, col))
        #set up labels
        self.turnLabel = Label(self, text="Turn: ")
        self.turnLabel['bg'] = 'white'
        self.turnLabel.grid(row=8, column=0)
        self.turnMarker = CheckerSquare(self, (8, 1))
        self.turnMarker['bg'] = 'lightgray'
        self.turnMarker.place_checker('red')
        self.turnMarker.select('black')
        self.turnMarker.color = None
        self.turn = 'red'
        self.infoLabel = Label(self, bg='white', text='', font=('Arial', 14, 'bold'))
        #place red checkers
        for a in range(3):
            for b in range(8):
                if self.squares[(a, b)]['bg'] == 'dark green':
                    self.squares[(a, b)].place_checker('red')
        #place white checkers
        for x in range(5, 8):
            for y in range(8):
                if self.squares[(x, y)]['bg'] == 'dark green':
                    self.squares[(x, y)].place_checker('white')

    def move_checker(self, checker, target):
        '''CheckerBoard.move_checker(checker, target)
        moves a checker fron checker to target by clearing the checker and creating a checker at target.
        checker and target must be CheckerSquare objects
        also handles moving king pieces'''
        color = checker.get_color()
        checker.clear()
        #if on the last row make a king
        if color == 'red' and target.get_coords()[0] == 7:
            target.set_king()
        elif color == 'white' and target.get_coords()[0] == 0:
            target.set_king()
        if checker.king:
            checker.king = False
            target.set_king()
        target.place_checker(color)

    def selected(self):
        '''CheckerBoard.selected() -> bool
        checks if any squares in the board are selected.'''
        for x in range(8):
            for y in range(8):
                if self.squares[(x, y)].is_selected():
                    return True
        return False

    def unselect_all(self):
        '''CheckerBoard.unselect_all()
        unselects all checkers in the board.'''
        for x in range(8):
            for y in range(8):
                self.squares[(x, y)].unselect()

    def is_valid_forward(self, checker, target):
        '''CheckerBoard.is_valid_forward(checker, target) -> bool
        checks if moving a checker from checker to target is a valid forward move
        checker and target must be CheckerSquare objects'''
        
        checkercoords = checker.get_coords()
        targetcoords = target.get_coords()
        checkerx = checkercoords[0]
        checkery = checkercoords[1]
        targetx = targetcoords[0]
        targety = targetcoords[1]
        if self.turn == 'red': 
            if target.is_empty(): #if target square is empty
                if checkerx - targetx in (1, -1) and checkery - targety in (1, -1): #if valid forward
                    if checker.is_king(): 
                        return True 
                    else: 
                        if targetx - checkerx == 1: 
                            return True 
        elif self.turn == 'white': 
            if target.is_empty(): #if the target square is empty
                if checkerx - targetx in (1, -1) and checkery - targety in (1, -1): #if valid forward 
                    if checker.is_king():
                        return True 
                    else: 
                        if checkerx - targetx == 1: 
                            return True 
        return False 

    def is_valid_jump(self, checker, target):
        '''CheckerBoard.is_valid_jump(checker, target) -> bool
        checks if moving a checker from checker to target is a valid jump move
        checker and target must be CheckerSquare objects'''
        checkercoords = checker.get_coords()
        targetcoords = target.get_coords()
        checkerx = checkercoords[0]
        checkery = checkercoords[1]
        targetx = targetcoords[0]
        targety = targetcoords[1]
        if self.turn == 'red': 
            if target.is_empty(): #if target square is empty
                if checkerx - targetx in (2, -2) and checkery - targety in (2, -2): #if valid jump 
                    if not self.squares[((checkerx + targetx)/2,
                    (checkery + targety)/2)].empty and self.squares[((checkerx + targetx)/2,
                    (checkery + targety)/2)].color == 'white': 
                        if checker.is_king(): 
                            return True 
                        else: 
                            if targetx - checkerx == 2: #if it is a jump
                                return True 
        elif self.turn == 'white': 
            if target.is_empty(): #if the target square is empty
                if checkerx - targetx in (2, -2) and checkery - targety in (2, -2): #if valid jump 
                    if not self.squares[((checkerx + targetx)/2,
                    (checkery + targety)/2)].empty and self.squares[((checkerx + targetx)/2,
                    (checkery + targety)/2)].color == 'red': #if square is not empty and the color is red
                        if checker.is_king(): 
                            return True 
                        else: 
                            if checkerx - targetx == 2: 
                                return True 
    
        return False 

    def get_valid_jumps(self):
        '''CheckerBoard.get_valid_jumps() -> int
        counts the total number of valid jumps throughout the whole board'''
        get_valid_jumps = 0
        if self.turn == 'red':
            #go through all the squares to get valid jumps
            for a in range(8):
                for b in range(8):
                    if not self.squares[(a, b)].is_empty() and self.squares[(a, b)].get_color() == 'red':
                        for x in range(8):
                            for y in range(8):
                                if self.squares[(x, y)].is_empty():
                                    if self.is_valid_jump(self.squares[(a, b)], self.squares[(x, y)]):
                                        get_valid_jumps += 1
           #same thing but with white
        elif self.turn == 'white':
            for a in range(8):
                for b in range(8):
                    if not self.squares[(a, b)].is_empty() and self.squares[(a, b)].get_color() == 'white':
                        for x in range(8):
                            for y in range(8):
                                if self.squares[(x, y)].is_empty():
                                    if self.is_valid_jump(self.squares[(a, b)], self.squares[(x, y)]):
                                        get_valid_jumps += 1
        return get_valid_jumps

    def valid_jump(self, checker):
        '''CheckerBoard.valid_jump(checker) -> int
        counts the number of valid jumps from a specific checker'''
        checker_coords = checker.get_coords()
        checkerx = checker_coords[0]
        checkery = checker_coords[1]
        valid_jump = 0
        #try and except for jumps
        for coord in ((checkerx + 2, checkery + 2), (checkerx + 2, checkery - 2), (checkerx - 2, checkery + 2), (checkerx - 2, checkery - 2)):
            try:
                if self.is_valid_jump(checker, self.squares[coord]):
                    valid_jump += 1
            except:
                pass
        return valid_jump

    def is_valid_move(self, checker, target):
        '''CheckerBoard.is_valid_move(checker, target) -> str
        returns 'jump' if it is a valid jump
        returns 'forward' if it is a valid forward move
        returns None if it is a valid forward move but you have to jump
        or it returns None because it isn't a valid move at all.'''
        if self.get_valid_jumps() > 0:
            self.infoLabel.grid(row=8, column=2, columnspan=6)#label for jump
            self.infoLabel['text'] = "Must jump enemy piece!" #must jump
            if self.is_valid_jump(checker, target):
                return 'jump'
        else:
            self.infoLabel['text'] = ''
            if self.is_valid_forward(checker, target):
                return 'forward' #valid forward move
        return None
        

    def valid_moves(self, color):
        '''CheckerBoard.valid_moves(color) -> int
        counts the number of valid moves for a certain color'''
        valid_moves = 0 
        for k in range(8):
            for l in range(8):
                if not self.squares[(k, l)].is_empty() and self.squares[(k, l)].get_color() == color: #if square is empty and color matches parameter
                    for m in range(8):
                        for n in range(8):
                            if self.squares[(m, n)].is_empty():
                                if self.is_valid_move(self.squares[(k, l)], self.squares[(m, n)]) in ('forward', 'jump'): #if move valide
                                      valid_moves += 1 
        return valid_moves #return valid_moves count

    def take_turn(self):
        '''CheckerBoard.take_turn()
        changes the turn, updates the turnMarker, and checks if someone won'''
        if self.turn == 'red':
            previousturn = self.turn
            self.turn = 'white'
            if self.valid_moves(self.turn) == 0:
                self.won(previousturn.capitalize())
            self.turnMarker.clear()
            self.turnMarker.place_checker(self.turn)#put checker on turn counter
            self.turnMarker.color = None

        else:
            previousturn = self.turn
            self.turn = 'red'
            if self.valid_moves(self.turn) == 0:
                self.won(previousturn.capitalize())
            self.turnMarker.clear()
            self.turnMarker.place_checker(self.turn)#put checker on turn counter
            self.turnMarker.color = None

    def won(self, color):
        '''CheckerBoard.won(color)
        updates the infoLabel grid position and text
        creates a messagebox info box saying who won'''
        #unbind all buttons
        for i in range(8):
            for j in range(8):
                self.squares[(i, j)].unbind('<Button>')
        self.infoLabel['text'] = "{0} wins!".format(color)
        self.infoLabel.grid(row=8, column=5, columnspan=3)
        #label
        messagebox.showinfo("{0} wins!".format(color), "{0}, you won! Good job!".format(color))


def play_checkers():
    '''checkers()
    starts a new game of checkers'''
    root = Tk()
    root.title("Checkers")
    checkers =  CheckerBoard(root)
    checkers.mainloop()


play_checkers()
