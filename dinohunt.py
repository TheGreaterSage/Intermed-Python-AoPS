import random
class Die:
    '''Die class'''

    def __init__(self,sides=6):
        '''Die(sides)
        creates a new Die object
        int sides is the number of sides
        (default is 6)
        -or- sides is a list/tuple of sides'''
        # if an integer, create a die with sides
        #  from 1 to sides
        if isinstance(sides,int):
            self.numSides = sides
            self.sides = list(range(1,sides+1))
        else:  # use the list/tuple provided 
            self.numSides = len(sides)
            self.sides = list(sides)
        # roll the die to get a random side on top to start
        self.roll()

    def __str__(self):
        '''str(Die) -> str
        string representation of Die'''
        return 'A '+str(self.numSides)+'-sided die with '+\
               str(self.get_top())+' on top'

    def roll(self):
        '''Die.roll()
        rolls the die'''
        # pick a random side and put it on top
        self.top = self.sides[random.randrange(self.numSides)]

    def get_top(self):
        '''Die.get_top() -> object
        returns top of Die'''
        return self.top

    def set_top(self,value):
        '''Die.set_top(value)
        sets the top of the Die to value
        Does nothing if value is illegal'''
        if value in self.sides:
            self.top = value


### end Die class ###

class DinoDie(Die):
    '''implements the dice for Dino Hunt'''
    def __init__(self, sides, color): 
        Die.__init__(self,sides)
        self.color = color
        
    def __str__(self):
        return ' A ' + self.color + ' die with a ' + self.get_top() + ' on top'
    
    def get_color(self):
        return self.color

class DinoPlayer:
    '''implements a player of Dino Hunt'''
    def __init__(self,name,score=0): 
        self.name = name
        self.score = score
        self.pile = []


    def __str__(self):
        return self.name + ' has ' + str(self.score) + ' point(s).'

    def get_name(self):
        '''DinoPlayer.get_name() -> str
        returns the player's name'''
        return self.name

    def get_score(self):
        '''DinoPlayer.get_score() -> int
        returns the player's score'''
        return self.score
    
    def reset_pile(self):
        self.pile = [] # first empty the pile
        for n in range(6):
            self.pile.append(DinoDie(['dino','dino','dino','leaf','leaf','foot'],'green'))
        for n in range(4):
            self.pile.append(DinoDie(['dino','dino','leaf','leaf','foot','foot'],'yellow'))
        for n in range(3):
            self.pile.append(DinoDie(['dino','leaf','leaf','foot','foot','foot'],'red'))
        random.shuffle(self.pile)
  
    def chooseDice(self):
        '''DinoPlayer.roll(DicePile) -> list
        returns a list of 3 (or fewer) dice from the DicePile after it removes those 3 from the DicePile and rolls them'''

        selectedDice = []
        if len(self.pile) >= 3:
            for i in range(3):
                selectedDice.append(self.pile.pop())
        elif len(self.pile) < 3:
            for i in range(len(self.pile)):
                selectedDice.append(self.pile.pop())
        for dice in selectedDice:
            dice.roll()
        return selectedDice

    def take_turn(self):
        self.reset_pile() # first reset the pile
               
        print(self.name + ", it's your turn.")
        
        # keeping counts for this turn
        dinoCount = 0
        footCount = 0
        
        greenCount = 6
        yellowCount = 4
        redCount = 3
        

        
        while True: # loop for one turn
            print("\nYou have " + str(len(self.pile)) + ' dice remaining. \n' +\
            str(greenCount) + ' green, ' + str(yellowCount) + ' yellow, ' +\
            str(redCount) + ' red')

            input('Press enter to select dice and roll')
            
            selectedDice = [] 
            selectedDice = self.chooseDice() # select and roll dice
            

            for dice in selectedDice:
                print(dice)
                
                if dice.get_top() == "dino": # carry out top face functionalities
                    dinoCount += 1
                    self.score += 1
                    #self.pile.remove(dice)
                elif dice.get_top() == "foot":
                    footCount += 1
                    #self.pile.remove(dice)
                elif dice.get_top() == "leaf":
                    self.pile.append(dice)
                
                if dice.get_color() == "green": # subtract from the color counts
                  greenCount -= 1
                elif dice.get_color() == "yellow":
                  yellowCount -= 1
                elif dice.get_color() == "red":
                  redCount -= 1
                
            print('This turn so far: ' + str(dinoCount) + ' dinos and ' + str(footCount) + ' feet.')

            if footCount >= 3: # check if stomped
                print('Too bad, you got stomped!')
                self.score = 0
                return self.score
                
            if len(self.pile) == 0:
                print('You have no dice remaining! Your turn is over.')
                return self.score
                
            
            rollAgain = input('Do you want to roll again (y/n)')
            if rollAgain.lower() == "n":
                return self.score
            elif rollAgain.lower() == "y":
                continue


        

        
def play_dino_hunt(numPlayers,numRounds):
    '''play_dino_hunt(numPlayer,numRounds)
    plays a game of Dino Hunt
      numPlayers is the number of players
      numRounds is the number of turns per player'''
                        
    playerList = []
    for n in range(numPlayers):
        name = input('Player ' + str(n+1) + ', please enter your name:') 
        playerList.append(DinoPlayer(name))

    roundNum = 1
    currentPlayerNum = 0
    playersGone = 0
    scoresList = [] # initialize list of scores
    for i in range(numPlayers): 
      scoresList.append(0)


    while True:
        if currentPlayerNum == 0:
            print('\n----- ROUND ' + str(roundNum) + ' -----')
        
        print('\n')
        for player in playerList:
            print(player)
        print('\n')

        scoresList[currentPlayerNum] = playerList[currentPlayerNum].take_turn()

        # check for a winner at the end only
        if roundNum == numRounds and currentPlayerNum == numPlayers-1:
            '''
            winnerIndex = scoresList.index(max(scoresList))
            print('\n' + playerList[winnerIndex].get_name() + " wins with " + str(playerList[winnerIndex].get_score()) + " points!") 
            '''
            winners = [player for player in playerList if player.get_score() == max(scoresList)]
            print('\nThe winner(s) is/are:')
            for player in winners:
                print(player.get_name())
            print('with ' + str(max(scoresList)) + ' point(s)!')
            if len(winners) > 1:
                print("It's a tie!")
            break
            
        # go to next player
        currentPlayerNum = (currentPlayerNum + 1) % numPlayers
        playersGone += 1
        # go to next round if all players have gone
        if playersGone == numPlayers:
            roundNum += 1
            playersGone = 0
        

play_dino_hunt(2,1)
