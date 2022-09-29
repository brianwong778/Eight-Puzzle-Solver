import random
from state import *
from board import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
    """
  
    def __init__(self,depth_limit):
        '''constructs a new Searcher object by initializing 3 attributes: 
           states, num_tested, and depth_limits
        '''
        self.states = [] # creates an empty list
        self.num_tested  = 0 # number tested starts at 0
        self.depth_limit = depth_limit # initializing depth_limit

  
    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s
    
    def should_add(self,state):
        '''takes a State object called state and returns True if the called 
           Searcher should add state to its list of untested states, and False
           otherwise.
           inputs: state is an object
        '''
        # cases in which searcher should not continue
        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        if state.creates_cycle():
            return False
        else: 
            return True
  
    def add_state(self,new_state):
        ''' takes a single State object called new_state and adds it to the 
            Searcher‘s list of untested states. 
        '''
        self.states += [new_state] # adds new_state to self
   
   
    def add_states(self,new_states):
        '''takes a list State objects called new_states, and processes
           the elements of new_states one at a time
           inputs: new_states is a list of objects
        '''
        # loops through new_states
        for i in range(len(new_states)):
            if self.should_add(new_states[i]) == True:
                self.add_state(new_states[i])
   
    def next_state(self):
        """ chooses the next state to be tested from the list of 
        untested states, then removes it from the list and returns
        """ 
        s = random.choice(self.states) # chooses a random state  
        self.states.remove(s) # removes that state
        return s
  
    def find_solution(self,init_state):
        '''performs random state-space search, and stops when the goal
           state is found or when the Searcher runs out of untested states.
           input:
               init_state is a parameter added to the untested states
        '''    
        self.add_state(init_state) # adds init_state parameter
        # loops while there are more states to go through
        while len(self.states) > 0:
            s = self.next_state()
            if s.is_goal() == True:
                self.num_tested += 1
                return s
            else:
                # continues to find successors
                self.num_tested += 1
                self.add_states(s.generate_successors())
            
        return None # failure
                
class BFSearcher(Searcher):
    '''A class that inherits from Searcher and uses first in first out to 
       solve the puzzle
    '''
    def next_state(self):
        '''Follows FIFO ordering, chooses the state that has been in the list 
           the longest
        '''
        s = self.states[0] # takes from the first state
        self.states.remove(s) # removes this state
        return s

class DFSearcher(Searcher):
    ''' A class that inherits from Searcher and uses last in last out to 
        solve the puzzle
     '''
    def next_state(self):
        '''follows LIFO ordering, chooses the state that was most recently 
           called
         '''
        s = self.states[-1] # takes from the last state
        self.states.remove(s) # removes this state
        return s
# heuristic functions
def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

def h1(state):
    '''find number of musplaced numbers'''
    return state.board.num_misplaced() 

def h2(state):
    '''number of misplaced tiles and moves required'''
    
    return state.board.num_misplaced_2()

class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
  
    def __init__(self, depth_limit, heuristic):
        """ constructor for a GreedySearcher object
        inputs:
         * depth_limit - the depth limit of the searcher
         * heuristic - a reference to the function to be used when computing 
         the priority of a state
        """

        Searcher.__init__(self,depth_limit)
        self.heuristic = heuristic
        
    def priority(self,state):
        ''' takes a State object called state, and that computes and
            returns the priority of that state.
        '''
        return -1 * self.heuristic(state)
    
    def add_state(self,state):
        '''Overrides the add_state method from Searcher. Adds a sublist in
          [priority, state] form, where priority is the priority of the
           state, determined by calling the priority method.
         '''
        self.states += [[self.priority(state),state]]
        
    def next_state(self):
        '''overrides the next_state method that is
           inherited from Searcher.
         '''
        # finds the sublist with highest priority
        s = max(self.states)
        # removes this sublist from the rest
        self.states.remove(s)
        return s[1]

    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s

class AStarSearcher(GreedySearcher):
    '''A class to solve the puzzle using heuristic functions
    '''
    
    def priority(self,state):
        '''assigns the priority based on a heuristic function, but also
           accounts for the amount of moves it takes
        '''
        return -1 * (self.heuristic(state) + state.num_moves)