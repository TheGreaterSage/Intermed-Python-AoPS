# Python Class 3251
# Lesson 10 Problem 1
# Author: famichao (560766)

from tkinter import *
from tkinter import messagebox
import random

class MinesweeperSquare(Label):
    '''represents a square in Minesweeper.'''
    def __init__(self, master, coord):
        '''MinesweeperSquare(master, coord) -> MinesweeperSquare
        creates a new MinesweeperSquare with (row, column) coord.'''
        Label.__init__(self, width=2, height=1, bg='white', bd=2, relief=RAISED, font=('Arial', 15))
        self.master = master
        self.coord = coord
        self.numAdj = 0
        self.isBomb = False
        self.isExposed = False
        self.isFlagged = False
        self.bind('<Button-1>', self.expose)
        self.bind('<Button-2>', self.set_flag)
        self.bind('<Button-3>', self.set_flag)

    def is_bomb(self):
        '''MinesweeperSquare.is_bomb() -> bool
        returns True if square contains a bomb, False otherwise.'''
        return self.isBomb

    def is_exposed(self):
        '''MinesweeperSquare.is_exposed() -> bool
        returns True if square is exposed, False otherwise.'''
        return self.isExposed

    def is_flagged(self):
        '''MinesweeperSquare.is_flagged() -> bool
        returns True if square is flagged, False otherwise.'''
        return self.isFlagged

    def get_coord(self):
        '''MinesweeperSquare.get_coord() -> tuple
        returns the coordinates of the square.'''
        return self.coord

    def get_numAdj(self):
        '''MinesweeperSquare.numAdj() -> int
        returns the number of adjacent squares which contain bombs.'''
        return self.numAdj

    def set_bomb(self):
        '''MinesweeperSquare.set_bomb()
        makes the target square a bomb'''
        self.isBomb = True

    def set_AdjBombs(self, n):
        '''MinesweeperSquare.set_AdjBombs(n)
        sets the number of adjacent squares with bombs as n.'''
        self.numAdj = n
        
    def expose(self, event):
        '''MinesweeperSquare.expose()
        handler method for expose click.'''

        # if square is exposed or flagged, do nothing
        if self.is_exposed() or self.is_flagged():
            return
        # if square is bomb, trigger explode function
        elif self.isBomb:
            self.master.explode()
        # if there are no adjacent bombs set number to zero 
        else:
            if self.numAdj == 0:
                self['relief'] = SUNKEN
                self['bg'] = 'lightgray'
                self.isExposed = True
                self.master.expose(self.coord)
            # if there are adjacent bombs use colormap for the corresponding number
            else:
                colormap = ['', 'blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'black', 'dim gray']
                self['fg'] = colormap[self.numAdj]
                self['text'] = str(self.numAdj)
                self['relief'] = SUNKEN
                self['bg'] = 'lightgray'
                self.isExposed = True
        # if all squares are exposed, win the game
        self.master.has_won()

    def set_flag(self, event):
        '''MinesweeperSquare.set_flag()
        handler method for flag click.'''
        # if square is not exposed and flagged, unflag
        if not self.isExposed:
            if self.isFlagged:
                self['text'] = ''
                self.isFlagged = False
                self.master.numRemaining += 1
                self.master.counterLabel['text'] = str(self.master.numRemaining)
            #if square is not flagged, flag
            else:
                self['text'] = '*'
                self.isFlagged = True
                self.master.numRemaining -= 1
                self.master.counterLabel['text'] = str(self.master.numRemaining)
                self.master.has_won()


class MinesweeperGrid(Frame):
    '''represents a grid in a game of Minesweeper.'''
    def __init__(self, master, width, height, numBombs):
        '''MinesweeperGrid(master, width, height, numBombs) -> MinesweeperGrid
        creates a new blank MinesweeperGrid
        width, height: int representing width and height
        numBombs: int representing the number of bombs in the grid.'''
        # initialize the frame
        Frame.__init__(self, master, bg='black')
        self.grid()
        # set variables
        self.width = width
        self.height = height
        self.numBombs = numBombs
        self.numRemaining = numBombs
        # dictionary for squares
        self.squares = {}

        # create grid with row*column squares
        for row in range(self.height):
            for column in range(self.width):
                coord = (row, column)
                self.squares[coord] = MinesweeperSquare(self, coord)
                self.squares[coord].grid(row=row, column=column)
        self.coordList = [coord for coord in self.squares]
        self.bombList = []
        
        # randomly create bombs by replacing them in the coord list
        for i in range(numBombs):
            coord = random.choice(self.coordList)
            self.bombList.append(coord)
            self.coordList.remove(coord)
        for i in self.bombList:
            self.squares[i].set_bomb()
        for coord in self.coordList:
            x = coord[0]
            y = coord[1]
            total_bombs = 0
            for c in [(x-1, y-1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]:
                if c in self.squares:
                    if self.squares[c].is_bomb():
                        total_bombs += 1
            # sets the number of adjacent squares that are bombs
            self.squares[coord].set_AdjBombs(total_bombs)
        # create label with remaining number of bombs
        self.counterLabel = Label(master, text=str(self.numRemaining), font=('Helvetica', 20))
        self.counterLabel.grid(row=height + 1, column=0, columnspan=width)

    def expose(self, coord):
        '''MinesweeperGrid.expose()
        exposes all adjacent squares to a blank square.'''
        x = coord[0]
        y = coord[1]
        # exposes adjacent squares
        for square in [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]:
            if square in self.squares:
                self.squares[square].expose('<Button-1>')# recursive call for auto-exposing

    def explode(self):
        '''MinesweeperGrid.explode()
        handler method for bomb explosion'''
        for bombs in self.bombList:
            if self.squares[bombs].is_bomb() == True:
                bomb = self.squares[bombs]
                bomb['bg'] = 'red'
        messagebox.showerror('Minesweeper','KABOOM! You lose.', parent=self)

    def has_won(self):
        '''MinesweeperGrid.has_won()
        checks if the player has won'''
        for coord in self.coordList:
            if not self.squares[coord].is_exposed():
                return
        messagebox.showinfo('Minesweeper','Congratulations -- you won!', parent=self)
        
            
        
def play_minesweeper(width, height, numBombs):
    '''play_minesweeper()
    plays Minesweeper'''
    root = Tk()
    root.title('Minesweeper')
    game = MinesweeperGrid(root, width, height, numBombs)
    root.mainloop()

    
play_minesweeper(12, 10, 15)
