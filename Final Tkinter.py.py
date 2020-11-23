from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import copy

class Connect4:
    """ This class creates the game Connect4 in the terminal
    with an inputed number of rows and cols
    """

    def __init__(self, width, height, window=None):
        """ the constructor for objects of type Board. Creates the parameters
        of the board using the inputed number of rows and cols.
        """
        self.width = width
        self.height = height
        self.data = [] # this will be the board
        for row in range( height ): # Counting up to given height
            boardRow = [] #creates board rows
            for col in range( width ): # Counting up to given width
                boardRow += [' '] # add a space to this row
            self.data += [boardRow] # add the created matrix to self.data

    def __repr__(self):
        """ this method returns a string representation
        for an object of type Board. Creating the basic structure.
        """
        s = ''
        for row in range( self.height ):
            s += '|' #For each row in height, create a divider
            for col in range( self.width ):
                s += self.data[row][col] + '|' #For each col add dividers as well
            s += '\n' #Then add new line to go down one row

        s += '--'*self.width + '-\n' #At bottom create 2 horizontal dividers
                                     #for each column, plus an additional one

        for col in range( self.width ):
            s += ' ' + str(col % 10) #for each col add numbers displaying its num
        s += '\n'
        return s

    def clear(self):
        '''This function clears the current board.
        '''
        self.data = [] #Clears data in board by assigning empty list
        self.fillEmptyBoard()

    def fillEmptyBoard(self):
        '''This function creates a new empty board. Does same thing as
        bottom part of __init__. It's literally the same code, so don't mark
        me down for comments John.
        '''
        for row in range( self.height ): # 6
            boardRow = []
            for col in range( self.width ): # 7
                boardRow += [' '] # add a space to this row
            self.data += [boardRow]

    def addMove(self,col,ox):
        '''This function adds the specified checker to the bottom of the
        specified column or at least above the last checker.
        '''
        if self.allowsMove(col) == True: #If allowsMove is true (I prefer
                                         #to keep the "== True" for readability)
                                         #Plus tbh it's more sexy
            for row in range( self.height ):
                if self.data[row][col] != ' ': #if there is no space in the spot
                    self.data[row-1][col] = ox #go up one and add a checker
                                               #Basically overwrites current
                                               #checkers in column
                    return (row - 1)
            self.data[self.height - 1][col] = ox  #then adds one to top
            return (self.height - 1)

    def allowsMove(self,col):
        '''This function checks to see if the move is legal within the game
        logic and whether it is within the parameters of the board.
        '''
        if 0 <= col < self.width:
            return self.data[0][col] == ' ' #if the column has an empty space
                                            #it returns true
        return False                        #otherwise it returns false

    def delMove(self,col):
        '''This function deletes the current highest checker on the specified
        column.'''
        for row in range(self.height):
            if self.data[row][col] != ' ': #if the current spot is not a space
                self.data[row][col] = ' ' #make it a space, overwrites all elements
                return
        self.data[self.height-1][col] = ' ' #erases that checker

    def isFull(self):
        '''This function checks to see if the entire board is full by iterating
        through each spot and looking for a space. If none are found, then the
        board is full.
        '''
        for row in range(0,self.height): #for each spot in row
            for col in range(0,self.width): #for each spot in column
                if self.data[row][col] in ' ': #if spot is empty
                    return False #it is not full
        return True #otherwise it is full

    def winsFor(self,ox):
        '''This function checks for the four possible win conditions (four in a
        row; either vertical, horizontal, or diagonal-both ways). It iterates
        through the board looking for each of the possible conditions.
        '''
        # check for horizontal wins
        for row in range(0,self.height): #iterate through rows
            for col in range(0,self.width-3): #iterates through columns (-3 to
                                              #eliminate part of board not relevant)
                if self.data[row][col] == ox and \
                self.data[row][col+1] == ox and \
                self.data[row][col+2] == ox and \
                self.data[row][col+3] == ox:
                #lines 108 to 111 check the specified checker in each spot
                    return True #if all of them found, return True
        #Checks for diagonal (NE to SW) wins
        for row in range(0,self.height-3):
            for col in range(0,self.width-3):
                if self.data[row][col] == ox and \
                self.data[row+1][col+1] == ox and \
                self.data[row+2][col+2] == ox and \
                self.data[row+3][col+3] == ox:
                    return True
        #Checks for diagonal (NW to SE) wins
        for row in range(0,self.height-3):
            for col in range(3,self.width):
                if self.data[row][col] == ox and \
                self.data[row+1][col-1] == ox and \
                self.data[row+2][col-2] == ox and \
                self.data[row+3][col-3] == ox:
                    return True
        #Checks for vertical wins
        for row in range(0,self.height-3):
            for col in range(0,self.width):
                if self.data[row][col] == ox and \
                self.data[row+1][col] == ox and \
                self.data[row+2][col] == ox and \
                self.data[row+3][col] == ox:
                    return True
        return False #if no wins, then return False

    def hostGame(self):
        '''This function brings all of the other functions together by calling
        them in a while loop within their respective if/else statements. Thus
        creating the game Connect4. The player can play the game as expected and
        also bring up an options menu for reseting the board, deleting a move,
        or quitting the game.
        '''
        whosTurn = 'X' #X always starts first
        while True:
            print(self) #print the board
            print('It is', whosTurn + "'s" , 'turn.')

            if self.isFull() == False: #if board is not full
                choiceRoice = int(input("What column do you choose (num)? "))
                #line 152 stores column that user chooses
                if self.allowsMove(choiceRoice) == True: #if move is allowed
                    self.addMove(choiceRoice, whosTurn) # add the move
                    print(self)
                    if self.winsFor(whosTurn) == True: #if user wins now
                        print("Game is over.", whosTurn , "won. Wow you actually won!")
                        break #end game
                    if whosTurn == 'X': #lines 160-163 switch the turn to other player
                        whosTurn = 'O'
                    elif whosTurn == 'O':
                        whosTurn = 'X'
                else:
                    print("You're stupid. Pick another column you dimwit")
                    continue #if move is not allowed, give the same player the turn again
            else:
                print('Game is over. Tie.')
                break #if board is full, it is a tie, end game


            if self.optionsMenu() == True: #if user requests more options

                if self.reset() == True:
                    self.clear() #clear the board if user selects reset

                if self.backMove() == True:
                    self.delMove(int(input('Which column? ')))
                    #line 178 deletes top checker on user's chosen column
                if self.quit() == True:
                    print("\nSee ya!")
                    break #if user selects quit, game ends

    def playGameWith(self, Player):
        '''This function brings all of the other functions together by calling
        them in a while loop within their respective if/else statements. Thus
        creating the game Connect4. The player can play the game as expected and
        also bring up an options menu for reseting the board, deleting a move,
        or quitting the game. This particular function utilizes the Player class
        to create a working AI for the player to play against.
        '''
        whosTurn = 'X' #X always starts first
        while True:
            print(self) #print the board
            print('It is', whosTurn + "'s" , 'turn.') #whos turn is it
            if whosTurn == 'O':
                if self.isFull() == False: #check to see if full
                    self.addMove(Player.nextMove(self), 'O') #adds AI move calling on nextMove
                    print(self)
                    if self.winsFor(whosTurn) == True: #if AI wins now
                        print("Game is over.", whosTurn , "won. Wow you actually won!")
                        break #end game
                    whosTurn = 'X' #change turns
                else:
                    print('Game is over. Tie.')
                    break #if board is full, it is a tie, end game
            elif whosTurn == 'X':
                if self.isFull() == False: #if board is not full
                    choiceRoice = int(input("What column do you choose (num)? "))
                    #line 152 stores column that user chooses
                    if self.allowsMove(choiceRoice) == True: #if move is allowed
                        self.addMove(choiceRoice, whosTurn) # add the move
                        print(self)
                        if self.winsFor(whosTurn) == True: #if user wins now
                            print("Game is over.", whosTurn , "won. Wow you actually won!")
                            break #end game
                        whosTurn = 'O'
                    else:
                        print("You're stupid. Pick another column you dimwit")
                        continue #if move is not allowed, give the same player the turn again
                else:
                    print('Game is over. Tie.')
                    break #if board is full, it is a tie, end game


                if self.optionsMenu() == True: #if user requests more options

                    if self.reset() == True:
                        self.clear() #clear the board if user selects reset

                    if self.backMove() == True:
                        self.delMove(int(input('Which column? ')))
                        #line 178 deletes top checker on user's chosen column
                    if self.quit() == True:
                        print("\nSee ya!")
                        break #if user selects quit, game ends


    def checkIfYes(self, ifYes):
        '''This function acts as a helper function to the four parts of the
        option menu below. It streamlines the yes/no process for each of the
        options and returning True if the user types 'yes'
        '''
        if ifYes == 'yes':
            return True
        else:
            return False

    def quit(self):
        '''This function asks the user if they want to quit.
        '''
        return self.checkIfYes(input("Or do you want to quit (type yes if so)? "))

    def reset(self):
        '''This function asks the user if they want to reset the board.
        '''
        return self.checkIfYes(input("Reset (type yes if so)? "))

    def backMove(self):
        '''This function asks the user if they want to delete a previous move.
        '''
        return self.checkIfYes(input("Delete a move (type yes if so)? "))

    def optionsMenu(self):
        ''' This function asks the user if they want to open additional options.
        '''
        return self.checkIfYes(input("Other options (type yes if so)? "))

class Player:
    def __init__(self, ox, tbt, ply):
        self.checker = ox
        self.breakTie = tbt
        self.difficulty = ply

    def scoresFor(self, board, ox, ply):
        '''This function takes in the board, specific checker, and the ply amount
        to recursively build and return a list of scores for each index for the
        board given. Utilizing deepcopy, it creates a copy of the board for both
        the AI and the opponent's turn to evaluate the score when the board is
        edited and potential moves are made.
        '''
        scores = board.width * [50] #Initial scores, as a default (ply 0)
        if ply == 0: #for ply 0
            for col in range(board.width): #iterate thru each col in width of board
                if board.allowsMove(col) != True:
                    scores[col] = -1 #As a default (ply 0), if move is not allowed

        if ply > 0:
            nextOX = 'X' if ox == 'O' else 'O' #switches turns, basic if/else
            for col in range(board.width):
                ghostBoard = copy.deepcopy(board) #create a working copy of board
                                                  #deepcopy to allow for funcs to
                                                  #be called on it
                if ghostBoard.allowsMove(col): #if move allowed
                    ghostBoard.addMove(col, ox) # add the move to copied board
                    if ghostBoard.winsFor(ox): #check for win
                        scores[col] = 100 #give that col a score of 100 if so
                        #break
                    else:
                        if ply > 1:
                            if ghostBoard.isFull(): # Need to re-check if board full
                                scores[col] = -1
                            else:
                                for opponentCol in range(board.width): #Now looking
                                                                       #at opponents
                                                                       #turn
                                    ghostBoard2 = copy.deepcopy(ghostBoard)
                                    #line 305 makes another copy of board but of
                                    #ghostboard so as to retain the moves made
                                    #this new ghost board is for the opponent
                                    if ghostBoard2.allowsMove(opponentCol):
                                        ghostBoard2.addMove(opponentCol, nextOX)
                                        if ghostBoard2.winsFor(nextOX):
                                            scores[col] = 0 #return 0 because thats
                                                            #a win for opponent
                                            break
                                        else:

                                            board2Scores = self.scoresFor(ghostBoard2, ox, ply - 1)
                                            #line 317 is the recursive piece
                                            scores[col] = 50 #if no win for opponent
                                    else:
                                        scores[col] = 50 #if move is not allowed,
                                                         #however it is not -1
                                                         #because it is a hypothetical
                                                         #move
                else:
                    scores[col] = -1 # invalid move
        return scores #at end, scoresFor returns list of scores

    def nextMove(self, board):
        '''nextMove returns the next best move for AI by running it through scoresFor
        and tiebreakMove with the inputted ply.
        '''
        return self.tiebreakMove(self.scoresFor(board,self.checker, self.difficulty))

    def tiebreakMove(self, scores):
        '''This function takes in the scores list made by scoresFor and returns
        the max score of the list in a list while also breaking any ties
        by choosing either the left-most, right-most, or random highest score
        based on input.
        '''
        index = [] #keep track of index scores
        for i, j in enumerate(scores): #iterate thru indexes and scores of scores
            if j == max(scores): #if specific score is biggest
                index += [i] # add that index to list
        if self.breakTie == 'Left':
            return min(index) #return left-most index
        elif self.breakTie == 'Right':
            return max(index) #return right-most index
        elif self.breakTie == 'Random':
            return random.choice(index) #return random index


def updateStatus(statusInfo, newStatus):
    '''Takes in conditions of board and writes on status entry what is happening'''
    statusInfo.set(newStatus) #change status to what is given

def quit(root):
    '''Destroys window and quits game'''
    root.quit()

def newGame():
    '''Creates a new game, taking in ply wanted and other nitpicky things that
    must happen at the start of each game'''
    global canvas, b, aiBoy, gameCompleted, plyObject #changes the local variables
                                                      #to allow use outside of function
    # Lines 376-384 do whatever is needed to initialize a new game...
    print('New Game!!') #not needed, just there to look sexy
    plyValue = int(plyObject.get()) #gets selected ply from spinbox as int
    gameCompleted = {'status': False, 'message': ''} #game is not completed
    b = Connect4(7,6) #call board
    aiBoy = Player('O', 'Random', plyValue) #get AI player with selected ply
    updMsg = 'New Game Selected - Difficulty (ply): ' + str(plyValue) #new msg
    updateStatus(statusInfo, updMsg) #update status entry with the new message
    drawBoard(canvas)


def drawBoard(canvas, rows=6, cols=7):
    '''Draws the typical, empty connect 4 board.'''
    global circles
    width = 450 #board width
    height = 300 #board height
    size = 9.5 #size of circles
    initialColor = '#e5dfdf'
    diameter = width / size
    circles = [] #we want a list for this so that we can create a uniform pattern of circles
    colors = [] #use this list to fill each circle with right color later
    y = 2.5 #starting distance from edge of canvas for y axis
    for row in range(rows):
        circleRow = [] #Use this list to create a matrix to create board of circles
        colorRow = [] #Use this list to fill in the colors for each circle in matrix
        x = 2.5 #starting distance for x axis
        for col in range(cols):
            circleRow += [canvas.create_oval(x, y, x + diameter, y + diameter, fill=initialColor)]
            #line above creates the circles using the specified distances between and from board in cols
            colorRow += [initialColor] #add those colors to each as well
            x += diameter + 19.6 #this specific decimal was used just to get the board right

        circles += [circleRow] #Adding circles in the rows now
        colors += [colorRow] #Adding colors there as well
        y += diameter + 3 #again, weird number, but it was what was needed to make it just right

def clickCircle(event, rows=6, cols=7):
    '''This function takes the click input of the user and makes the game work,
    checking if full, then adding player move to clicked column, then moves on
    to AI turn and then back around, doing all of the little stuff needed in between'''
    global lastx, lasty, canvas, circles, gameCompleted

    updateStatus(statusInfo, 'Thinking...')

    lastx, lasty = event.x, event.y #finds where player clicks
    print('X: {}, Y: {}'.format(lastx, lasty)) #displays click coordinates on
                                               #terminal, useful when creating the
                                               #board for coder

    width = 450
    size = 9.5
    diameter = width / size
    col = int(event.x / (diameter + 19.6)) #takes coord and makes it cols
    row = int(event.y / (diameter + 3)) #takes coord and makes it rows
    print('You clicked on the board\'s matrix: [Row: %s][Column: %s]' % (row, col))

    #lines 425 - 430:
    # "col" is the column that I want to fill, need to call the
    # Board's innards to tell me (1) if the move is allowed, and (2)
    # the REAL row that I need to fill in.. because I could be clicking on
    # a row which is either filled or way up too high..
    # The board game will return the row to populate

    if b.isFull():
        updateStatus(statusInfo, 'Tie Game.')
        gameCompleted['status'] = True #brings up pop-up
        gameCompleted['message'] = 'Tie Game'
    else:
        if b.allowsMove(col):
            boardRow = b.addMove(col, 'X') # add move for player
            canvas.itemconfig(circles[boardRow][col], fill='#0c9463')

            if b.winsFor('X'):  # if user wins now
                updateStatus(statusInfo, 'Wow! Somehow you won, nice job freak.')
                gameCompleted['status'] = True
                gameCompleted['message'] = 'You won surprisingly...'

            if not gameCompleted['status']:

                # AI will always play after human..

                # Play AI move below..
                if b.isFull():
                    updateStatus(statusInfo, 'Tie Game, unreal...')
                    gameCompleted['status'] = True
                    gameCompleted['message'] = 'Tie Game'
                else:
                    aiCol = aiBoy.nextMove(b)
                    aiRow = b.addMove(aiCol, 'O')

                    canvas.itemconfig(circles[aiRow][aiCol], fill='#2d334a')

                    if b.winsFor('O'): #if AI wins now
                        updateStatus(statusInfo, 'AI wins, typical.')
                        gameCompleted['status'] = True
                        gameCompleted['message'] = 'AI Wins - You Lose. Which was expected of course...'
        else:
            updateStatus(statusInfo, 'Invalid Move. You\'re stupid')

    # Check if the game is over at end, below
    if gameCompleted['status']:
        updateStatus(statusInfo, 'Game Over')
        # Display Dialog
        retry = messagebox.askretrycancel(
            title='Game Over',
            message=gameCompleted['message'],
            detail='What would you like to do?',
            icon='info')
#lines 479-483 is the pop-up
        if retry:
            newGame()
        else:
            quit(root)
        return
    updateStatus(statusInfo, 'Player\'s Turn')


def main():
    global plyObject, statusInfo, circles, b, aiBoy, gameCompleted, root, canvas
    circles = []
    b = {}
    aiBoy = {}
    gameCompleted = {'status': False, 'message': ''} #dictionary to check if game
                                                     #is over and change message to user
    root = Tk() #required to start Tk
    #root.geometry('640x450')
    root.title('Connect4 Game (Final)') #name of window

    # Label for the difficulty
    plyLabel = ttk.Label(root, text='Difficulty:', width=-1)
    plyLabel.grid(row=0, column=0, pady=2, sticky=W)

    # Game Difficulty
    plyObject = ttk.Spinbox(root, from_=0, to=4, values=[0,1,2,3,4])
    plyObject.grid(row=0, column=1, pady=2, sticky=W)
    plyObject.set(0)

    # New Game/Quit Buttons
    ngBtn = ttk.Button(root, text='New Game', command=newGame)
    quitBtn = ttk.Button(root, text='Quit', command=lambda: quit(root))

    # arranging above button widgets
    ngBtn.grid(row=0, column=2, sticky=EW, pady=2)
    quitBtn.grid(row=0, column=3, sticky=EW, pady=2)

    # Main Game Board area...
    frame = ttk.Frame(root, width=450, height=300, relief='sunken', borderwidth=2)
    frame.grid(column=0, row=1, columnspan=4, pady=2, padx=3)
    canvas = Canvas(frame, width=450, height=300)
    canvas.grid(column=0, row=1, sticky=(N, W, E, S))
    canvas.bind("<Button-1>", clickCircle)

    # Label for the Status..
    statusLabel = ttk.Label(text='Status:')
    statusLabel.grid(row=2, column=0, pady=2, sticky=W)
    statusInfo = StringVar() #creates editable string variable, empty at start
    statusInfo.set('Game Started.')
    statusEntry = ttk.Entry(root, textvariable=statusInfo, state='readonly', width=40)
    statusEntry.grid(row=2, column=1, columnspan=3, sticky=W)

    newGame() #runs new game right off bat

    root.mainloop() #creates mainloop for window, required for it to work

if __name__ == '__main__':
    main()
