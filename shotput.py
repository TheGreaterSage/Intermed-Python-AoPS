from tkinter import *
import random

class GUIDie(Canvas):
    '''6-sided Die class for GUI'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self,master,width=60,height=60,bg='white',\
                        bd=5,relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top-1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1,7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1,1)],
                   [(0,0),(2,2)],
                   [(0,0),(1,1),(2,2)],
                   [(0,0),(0,2),(2,0),(2,2)],
                   [(0,0),(0,2),(1,1),(2,0),(2,2)],
                   [(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])

    def draw_pip(self,location,color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx,centery) = (17+20*location[1],17+20*location[0])  # center
        self.create_oval(centerx-5,centery-5,centerx+5,centery+5,fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)

class ShotPutFrame(Frame):
    '''frame for a game of Shot Put'''

    def __init__(self, master, name):
        '''ShotPutFrame(master,name) -> ShotPutFrame
        creates a new Shot Put frame
        name is the name of the player'''
        # set up Frame object
        Frame.__init__(self, master)
        self.grid()
        # label for player's name
        Label(self,text=name,font=('Arial',12)).grid(columnspan=3,sticky=W)
        # set up the attempt number, score, high score
        self.attemptScoreLabel = Label(self,text='Attempt #1 Score: 0',font=('Arial',12))
        self.attemptScoreLabel.grid(row=0,column=3,columnspan=2)
        self.highLabel = Label(self,text='High Score: 0',font=('Arial',12))
        self.highLabel.grid(row=0,column=5,columnspan=3,sticky=E)
        # initialize game data
        self.score = 0
        self.attemptNum = 1
        self.highScore = 0
        self.currentDieNum = 0
        self.scoreList = []
        # set up dice
        self.dice = []
        for n in range(8):
            self.dice.append(GUIDie(self,[1,2,3,4,5,6],['red']+5*['black']))
            self.dice[n].grid(row=1,column=n)
        # set up buttons
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=2,columnspan=1)
        self.stopButton = Button(self,text='Stop',state=DISABLED, command = self.stop)
        self.stopButton.grid(row=3,columnspan=1)

    def has_fouled(self):
        '''ShotPutFrame.has_fouled()
        returns True if player has rolled number 1
        returns False if not'''
        if self.currentDieNum > 7:
            return (self.dice[self.currentDieNum-1].get_top() == 1)
        else:
            return (self.dice[self.currentDieNum].get_top() == 1)

    def roll(self):
        '''ShotPutFrame.roll()
        handler method for the roll button click'''
        # roll current die
        self.dice[self.currentDieNum].roll()
        # turn on the stop button
        self.stopButton['state'] = ACTIVE
        # checks if the player has fouled
        if self.has_fouled() == True:
            self.attemptScoreLabel['text'] = 'FOULED ATTEMPT'
            self.stopButton['text'] = 'FOUL'
            self.rollButton['state'] = DISABLED
            self.score = 0
        else:
            # add dice to score and update the scoreboard
            self.score += self.dice[self.currentDieNum].get_top()
            self.attemptScoreLabel['text'] = 'Attempt #'+str(self.attemptNum)+' Score: '+str(self.score)
            self.currentDieNum += 1 # go to the next die
            if self.currentDieNum < 8: # move buttons to next die
                self.rollButton.grid(row=2,column=self.currentDieNum,columnspan=1)
                self.stopButton.grid(row=3,column=self.currentDieNum,columnspan=1)
                self.rollButton['state'] = ACTIVE
            else:
                self.rollButton['state'] = DISABLED
        if self.currentDieNum > 7:
            # if you have rolled 7 dice without a foul
            # roll the 8th
            self.dice[self.currentDieNum-1].roll()
            # if they fouled this time, 
            if self.has_fouled() == True:
                self.attemptScoreLabel['text'] = 'FOULED ATTEMPT'
                self.stopButton['text'] = 'FOUL'
                self.rollButton['state'] = DISABLED
                self.score = 0
            else:
                self.score += self.dice[self.currentDieNum-1].get_top()
                self.attemptScoreLabel['text'] = 'Attempt #'+str(self.attemptNum)+' Score: '+str(self.score)
                self.rollButton['state'] = DISABLED 

    def stop(self):
        '''ShotPutFrame.stop()
        handler method for the stop button click'''
        if self.attemptNum < 3:
            # Increase attempt num
            self.attemptNum += 1
            # delete the dice, recreate them again
            for die in self.dice:
                die.destroy()
            self.dice = []
            for n in range(8):
                self.dice.append(GUIDie(self,[1,2,3,4,5,6],['red']+5*['black']))
                self.dice[n].grid(row=1,column=n)
            # check for a high score
            self.scoreList.append(self.score)
            self.highScore = max(self.scoreList)
            # reset score
            self.score = 0
            self.currentDieNum = 0
            # reset the score labels
            self.attemptScoreLabel['text'] = 'Attempt #'+str(self.attemptNum)+' Score: 0'
            self.highLabel['text'] = 'High Score: '+str(self.highScore)
            # reset button positions and states
            self.rollButton.grid(row=2,column=self.currentDieNum,columnspan=1)
            self.stopButton.grid(row=3,column=self.currentDieNum,columnspan=1)
            self.rollButton['state'] = ACTIVE
            self.stopButton['state'] = DISABLED
            self.stopButton['text'] = 'Stop'
        else:
            self.attemptScoreLabel['text'] = 'Game Over!'
            # check for a high score
            self.scoreList.append(self.score)
            self.highScore = max(self.scoreList)
            self.highLabel['text'] = 'High Score: '+str(self.highScore)
            self.rollButton.grid_forget()
            self.stopButton.grid_forget()
