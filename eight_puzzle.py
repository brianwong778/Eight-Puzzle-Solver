from searcher import *
from timer import *

def create_searcher(algorithm, depth_limit = -1, heuristic = None):
    """ a function that creates and returns an appropriate searcher object, 
        based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm to use
          * depth_limit - an optional parameter that specifies a depth limit 
          * heuristic - an optional parameter that passes in a heuristic method
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(depth_limit)
    elif algorithm == 'BFS':
        searcher = BFSearcher(depth_limit)
    elif algorithm == 'DFS':
        searcher = DFSearcher(depth_limit)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(depth_limit, heuristic)
    elif algorithm == 'A*':
        searcher = AStarSearcher(depth_limit, heuristic)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, depth_limit = -1, heuristic = None):
    """ a driver function for solving 8 Puzzles that uses state-space search
        inputs:
          * init_boardstr - a string of digits that specifies the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm to use
          * depth_limit - an optional parameter that specifies a depth limit
          * heuristic - an optional parameter that passes in a heuristic method
    """
    
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')

    searcher = create_searcher(algorithm, depth_limit, heuristic)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()
            
def process_file(filename, algorithm, depth_limit=-1, heuristic=None):
        """ Opens a file 'filename' and solves it using specified algorithm
            with default inputs depth_limit = -1 and heuristic = None
        """
        # opens file for processing
        f = open(filename,'r')
        puzzles = 0
        moves = 0
        states_tested = 0
        
        # loops through the file 
        for line in f:
            string = str(line[:-1])
            board = Board(string) # creates Board object
            algorithm = str(algorithm) # finds algorithm used
            state = State(board,None,'init') # creates State object
            # calls create_searcher
            searcher = create_searcher(algorithm,depth_limit,heuristic)
            
            # looks for solution, soln is None by default
            soln = None
            try:
                soln = searcher.find_solution(state)
                # if search is None, prints the result
                if soln == None:
                    print(string + ': no solution')
                else:
                    # prints the string, number of moves needed, states tested 
                    print(string + ':', soln.num_moves, 'moves,', searcher.\
                          num_tested, 'states tested')
                    # updates the variables
                    puzzles += 1
                    moves += soln.num_moves
                    states_tested += searcher.num_tested
                
            except KeyboardInterrupt: # search is terminated 
               print(string + ':'  + ' search terminated, no solution')
               soln = None
                
        # output at the bottom
        if puzzles != 0:
            print()
            print('solved ',puzzles,'puzzles')
            print('averages:',moves/puzzles,'moves, ',states_tested/puzzles,\
                  'states tested')
        else:
            print('solved: 0 puzzles')
        
        