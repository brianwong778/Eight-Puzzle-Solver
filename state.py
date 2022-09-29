from board import *

# a 2-D list of the goal state
GOAL_TILES = [[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8]]

# the list of possible moves, that moves the blank cell in the specified 
# direction
MOVES = ['up', 'down', 'left', 'right']


class State:
    """ A class for objects that represent a state in the state-space 
        search tree of an Eight Puzzle.
    """

    def __init__(self,board,predecessor,move):
        """constructor that uses self to define board, predecessor, move
            inputs:
                * board - the playing board
                * predecessor - the previous puzzle configuration.
                * move - the move it took to get to the current state
        """
        self.board = board
        self.predecessor = predecessor
        self.move = move
        # initial case, there is no predecessor
        if predecessor == None:
            # counts the number of moves done, starts at 0
            self.num_moves = 0
        else: # not the inital case
            # adds one to the count
            self.num_moves = predecessor.num_moves + 1
    

    def is_goal(self):
        '''checks if the current board is the goal state
        '''
        # returns a Boolean value if the board is the same as the GOAL_TILES
        return self.board.tiles == GOAL_TILES
    
   
    def generate_successors(self):
        '''takes the current board and checks for all possible cases after a 
           move, then adds that possible case to a list
        '''
        # creates a blank list 
        successors = []
        # loops through the list of valid moves
        for m in MOVES:
            # creates a copy of the board
            b = self.board.copy()
            # checks each move to see if it is a valid move on the current 
            # board
            if b.move_blank(m) == True :
                # sets a variable to a new State object created after moving 
                # the board
                new = State(b, self, m)
                # adds new board to the list of successors
                successors += [new]
        return successors
                
    
    def __repr__(self):
        """ returns a string representation of the State object
            referred to by self.
        """
   
        s = self.board.digit_string() + '-'
        s += self.move + '-'
        s += str(self.num_moves)
        return s
    
    def creates_cycle(self):
        """ returns True if this State object would create a cycle 
            in the current sequence of moves,
            and False otherwise.
        """
        state = self.predecessor
        while state != None:
            if state.board == self.board:
               return True
            state = state.predecessor
        return False

    def __gt__(self, other):
        """ implements a > operator for State objects
            that always returns True. This is used to break
            ties when max() is called on a list of [priority, state] pairs.
        """
        return True
    
    def print_moves_to(self):
        '''prints inital board and all neccessary steps to solve it, as well as
           the board at each step
        '''
        if self.predecessor == None: # if this is the inital board, base case
            print('initial state') # labels it the inital board
            print(self.board) # prints the inital board
        else: # recursive case
            # recursively calls the method to find the rest 
            self.predecessor.print_moves_to()
            # prints the move needed
            print('move the blank ' + self.move)
            # prints a copy of the board at the case
            print(self.board)
            
