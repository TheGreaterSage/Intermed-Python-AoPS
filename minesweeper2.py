### MINESWEEPER ###
from tkinter import *
from tkinter import messagebox
import random

class MSCell(Label):
    '''Represents a Minesweeper Cell'''

    def __init__(self,master,row,column,adjacentBombs,isBomb):
        '''MSCell(master,row,column,adjacentBombs,isBomb) -> MSCell
        creates a new blank MSCell with row and column
        adjacentBombs and isBomb'''
        Label.__init__(self,master,height=1,width=2,text='',\
                       bg='gray',font=('Arial',24),relief=RAISED)
        self.row = row
        self.column = column
        self.coord = (row,column)
        self.adjacentBombs = adjacentBombs
        self.hidden = True
        self.isflagged = False
        self.isBomb = isBomb
        # Set up listeners
        self.bind('<Button-1>', self.update_display_clicked)
        self.bind('<Button-2>', self.displayBomb)
        self.bind('<Button-3>', self.displayBomb)

    def getcoord(self):
        '''Accessor Method'''
        return (self.row,self.column)

    def adjacentBombs(self):
        '''Accessor Method'''
        return adjacentBombs

    def isHidden(self):
        '''Accessor Method'''
        return self.hidden

    def isEvil(self):
        '''Accessor Method'''
        return self.isBomb

    def displayBomb(self, event):
        '''Shows a bomb
        Handler method for right click'''
        if self['text'] == '*':
            self.master.bombsLeft += 1
            self['text'] = ''
        else:
            self.master.bombsLeft -= 1
            self['text'] = '*'

    def __eq__(self,other):
        if self.row == other.row and self.column == other.column:
            return True
        else:
            return False

    def reveal(self):
        '''Reveals the cell when clicked
        Handler method for left click'''  
        if self.adjacentBombs != '*' and self.adjacentBombs != 0:
            colorKey = ['', 'blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'black', 'dim gray']
            self['fg'] = colorKey[self.adjacentBombs]
            self['bg'] = 'lightgray'
            self['text'] = self.adjacentBombs
            self.hidden = False
            self['relief'] = SUNKEN
            self.master.cellsLeft -= 1
            if self.master.cellsLeft == 0:
                self.master.win_game()

    def showAdjacentSquares(self):
        '''If revealed, but has no adjacent bombs
        Used with reveal'''
        height = self.master.height
        width = self.master.width
        cellDict = self.master.cells
        for r in range(-1, 2):
            for c in range(-1, 2):
                if 0 <= self.row+r and self.row+r < height and 0 <= self.column+c and self.column+c < width:
                    otherCell = cellDict[(self.row+r,self.column+c)]
                    if otherCell.isHidden() and not otherCell.isBomb:
                        otherCell.reveal()

    def update_display_clicked(self,event):
        '''Changes the display of the clicked MSCell
        Also displays the number'''
        self.reveal()
        self['bg'] = 'lightgray'
        if self.adjacentBombs == '*': # meaning we lose
            self['text'] = self.adjacentBombs
            self.master.lose_game()
 
        elif self.adjacentBombs == 0:
            self.showAdjacentSquares()

class MSGrid(Frame):
    '''Represents a grid of MSCells'''

    def __init__(self, master, width, height, numBombs):
        '''MSGrid(master,width,height,numBombs) -> MSGrid
        Creates a new MSGrid with width, height, numBombs'''
        Frame.__init__(self, master, bg = 'black')
        self.grid()
        self.width = width
        self.height = height
        self.numBombs = numBombs
        self.bombsLeft = numBombs
        # create the cells
        self.cells = {}
        self.coordList = []
        for r in range(height):
            for c in range(width):
                coord = (r,c)
                self.coordList.append(coord)
        self.normalList = self.coordList[:]
        self.bombList = []
        for bomb in range(self.numBombs):
            randomValue = random.choice(self.normalList)
            self.bombList.append(randomValue)
            self.normalList.remove(randomValue)
        # grid the bombs first
        for bomb in self.bombList:
            self.cells[bomb] = MSCell(self,bomb[0],bomb[1],'*', True)
            self.cells[bomb].grid(row=bomb[0], column=bomb[1])
        # then grid the rest
        for cell in self.normalList:
            self.cells[cell] = MSCell(self,cell[0],cell[0],self.numAdjacentBombs(cell),False)
            self.cells[cell].grid(row=cell[0],column=cell[1])
        self.cellsLeft = len(self.normalList)
        # set up flag label
        flagLabel = Label(master, text=self.bombsLeft, bg='white', fg='black',font=('Arial', 12))
        flagLabel.grid(row=self.width//2, column=self.height+1, columnspan=self.width)

    def numAdjacentBombs(self,coord):
        '''Returns the number of adjacent bombs'''
        numBombs = 0
        for r in range(-1, 2):
            for c in range(-1, 2):
                if 0 <= coord[0]+r and coord[0]+r < self.height and 0 <= coord[1]+c and coord[1]+c < self.width:
                    string = (r,c)
                    if string in self.bombList:
                        numBombs += 1
        return numBombs

    def win_game(self):
        '''If no bombs are left, and everything is revealed'''
        messagebox.showinfo("Minesweeper", "Congratulations -- you won!", parent=self)

    def lose_game(self):
        '''If you revealed a bomb'''
        messagebox.showerror("Minesweeper", "KABOOM! You lose.", parent=self)
        self.show_bombs()

    def show_bombs(self):
        '''Show all the bombs in red'''
        for cell in self.cells:
            if self.cells[cell].isBomb:
                self.cells[cell]['bg'] = 'red'
                self.cells[cell]['text'] = '*'
                   
root = Tk()
root.title('Minesweeper')
pot = MSGrid(root,5,5,3)
pot.grid(row=0,column=0)
root.mainloop()
