class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles=[[0] * 3 for x in range(3)]
        self.blank_r=-1
        self.blank_c=-1
        
        for r in range(0,3):
            for c in range(0,3):
                self.tiles[r][c]=int(digitstr[3*r + c])
                if self.tiles[r][c] == 0:
                    self.blank_r=r
                    self.blank_c=c
                    
    def __repr__(self):
        '''returns a string representation of a Board object.
        '''
        s=''
        for r in range(0,3):
            for c in range(0,3):
                if self.tiles[r][c] != 0:
                    s += str(self.tiles[r][c]) + ' '
                else:
                    s += '_ '
            s += '\n'
            
        return s
    
    def move_blank(self,direction):
        ''' moves the blank space within the grid with input direction
            inputs: direction is the desired direction to move the blank
            space
        '''
        new_row=0
        new_col=0
        
        # upwards
        if(direction =='up'):
            # finds the coordinates of an up move, saves in temp. variables
            new_row = self.blank_r - 1
            new_col = self.blank_c
            # checks if new coordinates are within the grid
            if(new_row < 0 or new_row > 2):
                return False # returns False if moving upwards is not possible
                
        # down    
        elif(direction == 'down'):
            # finds the coordinates of a down move, saves in temp. variables
            new_row = self.blank_r + 1
            new_col = self.blank_c
            # checks if new coordinates are within the grid
            if(new_row < 0 or new_row > 2):
                return False
        # leftward 
        elif(direction=='left'):
            # finds the coordinates of a left move, saves in temp. varibales
            new_row = self.blank_r
            new_col = self.blank_c-1
            # checks if new coordinates are within the grid
            if(new_col<0 or new_col>2):
                return False
            
        # rightwards
        elif(direction == 'right'):
            # finds the coordinates of a left move, saves in temp. varibales
            new_row = self.blank_r
            new_col = self.blank_c + 1
            # checks if new coordinates are within the grid
            if(new_col<0 or new_col>2):
                return False
            
        # switches the value in the old blank coordinates to the value at the 
        # place in which the blank needs to take
        self.tiles[self.blank_r][self.blank_c]=self.tiles[new_row][new_col]
        # sets new coordinates to 0
        self.tiles[new_row][new_col] = 0
        # updates the blank row and column
        self.blank_c = new_col
        self.blank_r = new_row
        return True
    
    def digit_string(self):
        '''converts the board to a string representation
        '''
        s= ''
        # loops through the board
        for r in range(0,3):
            for c in range(0,3):
                # adds each character in the board to the string sequentially
                s += str(self.tiles[r][c]) 
        return s
    
    def copy(self):
        '''creates a deep copy of self
        '''
        # creates a deep copy by creating a new board with the same 
        # digit_string input
        board_copy = Board(self.digit_string())
        return board_copy
    
    def num_misplaced(self):
        ''' returns the number of values in the wrong position
        '''
        count = 0
        # loops through the board
        for r in range(0,3):
            for c in range(0,3):
                # does not include 0
                if self.tiles[r][c] != 0:
                    # uses formula to check if the position has the right value
                    if self.tiles[r][c] != r * 3 + c:
                        count +=1
        return count
    
    def __eq__(self,other):
        '''allows == to override and check if two boards are the same
           inputs:
               other is the second board to check against
        '''
        # checks if self and other are equal using their digit strings
        if self.digit_string() == other.digit_string():
            return True
        else:
            return False
        
    def num_misplaced_2(self):
        """ returns a new number as priority. If a number is not at the correct
            place (using GOAL_TITLES as reference), num_misplaced_2 will get the
            necessary value from the correct column and row. 
        """
        goal_tiles = [[0, 1, 2],
                      [3, 4, 5],
                      [6, 7, 8]]
        
        new = 0
        # loops through the tiles
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[0])):
                board_tiles = self.tiles[row][col]
                # checks if tiles are not the goal tiles
                if board_tiles != goal_tiles[row][col]:
                    # adds the absolute value of the row - board tiles // 3
                    new += abs(row - board_tiles // 3)
                     # adds the col - board tiles modulo 3
                    new += abs(col - board_tiles % 3)
                else:
                    None
        return new 
        
       
 
        


        
        
                    