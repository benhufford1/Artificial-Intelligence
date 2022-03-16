import numpy as np

rows = 24
cols = 24
alpha = .9
gamma = .9
epsilon = .2


def create_board(rows, cols): 
    '''creates a list of lists, where the [i][j] element
    in the board is the reward of state (i,j). [0][0] is the top left of the 
    gridworld.'''
    board = []
    for i in range(rows): 
        board.append([-1]*cols)
    for i in range(1,24): 
        board[i][7] = -100
    for i in range(0,23): 
        board[i][14] = -100
    board[0][23] = 100
    return board

def init_states(rows, cols): 
    """ creates a list of tuples, each tuple is (i,j) for row i, column j"""
    states = []
    for row in range(rows): 
        for col in range(cols): 
            states.append((row, col))
    return states
                     
def state_action_pairs(states):
    '''takes in a list of tuple states, returns a list of states-action pairs 
    (each s-a pair is a sublist). Each sublist contains a tuple state as its
    first element and 'up', 'down', 'left', 'right' as its second element'''
    s_a_pairs = []
    for state in states: 
        s_a_pairs.append([state, 'up']) 
        s_a_pairs.append([state, 'down'])
        s_a_pairs.append([state, 'left'])
        s_a_pairs.append([state, 'right'])
    return s_a_pairs
      
def init_q_matrix(s_a_pairs):
    """takes in list of lists for state-action pairs and assigns a random value
    in [0,1], then stores str(list) as a dict key to locate that q-value"""
    q_matrix = {}
    for pair in s_a_pairs: 
        q_matrix[str(pair)] = np.random.rand()
    return q_matrix

def max_q_val(state, q_matrix): 
    """state is tje state tuple from states, returns the maximum q-val from 
    q-val matrix corresponding to that state, and the corresponding state-action list"""
    q = -100000
    max_s_a_pair = None
    for action in ['up', 'down', 'left', 'right']:
        if q_matrix[str([state, action])] > q: 
            q = q_matrix[str([state, action])]
            max_s_a_pair = [state, action]
    return max_s_a_pair, q

def new_state(s_a_pair): 
    """takes in a list of state (tuple) and action (string) and returns the 
    tuple location that that state-action pair moves the agent to"""
    if s_a_pair[1] == 'up': 
        if s_a_pair[0][0] == 0: 
            n_state = s_a_pair[0]
        else: 
            n_state = (s_a_pair[0][0] - 1,s_a_pair[0][1])
    if s_a_pair[1] == 'down': 
        if s_a_pair[0][0] == 23: 
            n_state = s_a_pair[0]
        else: 
            n_state = (s_a_pair[0][0] + 1,s_a_pair[0][1])
    if s_a_pair[1] == 'left': 
        if s_a_pair[0][1] == 0: 
            n_state = s_a_pair[0]
        else: 
            n_state = (s_a_pair[0][0],s_a_pair[0][1] - 1)
    if s_a_pair[1] == 'right': 
        if s_a_pair[0][1] == 23: 
            n_state = s_a_pair[0]
        else: 
            n_state = (s_a_pair[0][0],s_a_pair[0][1] + 1)
    return n_state
 
def update_q_val(s_a_pair):   
    """updates the q_val of a state-action pair based on the reward and possible
    future reward of that state-action pair"""
    n_state = new_state(s_a_pair)
    old_q = q_matrix[str(s_a_pair)]
    reward = board[n_state[0]][n_state[1]]
    pair, max_q = max_q_val(n_state, q_matrix)
    new_q = old_q + alpha*(reward+gamma*max_q - old_q)
    q_matrix[str(s_a_pair)] = new_q
    return old_q, new_q

def choose_next_action(state, epsilon): 
    '''takes in a tuple state and returns a state-action pair (list), either 
    a random action with probability epsilon, or a deterministic (largest q-val) 
    action with probability 1 - epsilon'''
    choice = np.random.choice(['random', 'deterministic'], p=(epsilon, 1-epsilon))
    if choice == 'random': 
        action = np.random.choice(['up', 'down', 'left', 'right'])
        new_pair = [state, action]
    if choice == 'deterministic': 
        action, q = max_q_val(state, q_matrix)
        new_pair = [state, action[1]]
    return new_pair


def k_rand_walks(start, k, epsilon): 
    """runs k random walks to train q-values. For the first 800 walks, it uses 
    e-greedy algorithm, with some randomness. For walks beyond 800, it switches 
    to greedy algorithm. Once the greedy algorithm returns the same path 30 times 
    in a row, it returns that path and the number of iterations it took to get there"""
    path_history = [0]*30
    for i in range(k): 
        #print("starting walk " + str(i))
        path = []
        state = start
        if i<800:
            e = epsilon
        else: 
            e = 0
        while state not in end_states: 
            s_a_pair=choose_next_action(state, e)
            n_state = new_state(s_a_pair)
            update_q_val(s_a_pair)
            path.append(s_a_pair)
            state = n_state
        path_history.append(path)
        path_history.pop(0)
        all_same = all(element == path_history[0] for element in path_history)
        #print(path)
        if all_same: 
            return 'final path: ', path_history[29], ' after ', i, ' iterations'
    return q_matrix

board = create_board(rows, cols)
states = init_states(rows, cols)
end_states = [(0,23)]
for i in range(1,24): 
    end_states.append((i, 7))
for i in range(0,23): 
    end_states.append((i, 14))
s_a_pairs = state_action_pairs(states)    
q_matrix = init_q_matrix(s_a_pairs)
x =  k_rand_walks((23,0), 2000, epsilon)
print(x) 