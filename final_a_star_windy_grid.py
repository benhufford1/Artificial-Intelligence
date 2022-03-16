
from  search_algorithm_09012021 import *

class Windy_State(Problem_State): 
    def __init__(self, state): 
        """state is a tuple, x is rows starting from 0, y is columns from 0, top left is (0,0)"""
        self.row = state[0]
        self.col = state[1]
        self.operator_list = ['moveup', 'movedown', 'moveleft', 'moveright']
        
    def __str__(self): 
        state_string = '(' + str(self.row)+','+str(self.col) + ')'
        return state_string
    
    def illegal(self): 
        if self.row < 0 or self.col < 0 or self.row > 6 or self.col > 9: 
            return True
        else: 
            return False 
        
    def equals(self, state): 
        if self.row == state.row and self.col == state.col: 
            return True
        else: 
            return False 
    
    def operator_names(self): 
        return self.operator_list 
    
    def moveup(self): 
        n_state = (self.row -1, self.col) 
        if n_state[1] in [3,4,5,8]: 
            if n_state[0] == 0: 
                n_state = n_state
            else: 
                n_state = (n_state[0] - 1, n_state[1])
        if n_state[1] in [6,7]: 
            if n_state[0] == 0 or n_state[0]==1:
                n_state = (0, n_state[1])
            else:  
                n_state = (n_state[0] - 2, n_state[1])
        return Windy_State(n_state)
    def movedown(self): 
        n_state = (self.row +1, self.col) 
        if n_state[1] in [3,4,5,8]: 
            if n_state[0] == 0: 
                n_state = n_state
            else: 
                n_state = (n_state[0] - 1, n_state[1])
        if n_state[1] in [6,7]: 
            if n_state[0] == 0 or n_state[0]==1:
                n_state = (0, n_state[1])
            else:  
                n_state = (n_state[0] - 2, n_state[1])
        return Windy_State(n_state)
    def moveleft(self):
        n_state = (self.row, self.col - 1) 
        if n_state[1] in [3,4,5,8]: 
            if n_state[0] == 0: 
                n_state = n_state
            else: 
                n_state = (n_state[0] - 1, n_state[1])
        if n_state[1] in [6,7]: 
            if n_state[0] == 0 or n_state[0]==1:
                n_state = (0, n_state[1])
            else:  
                n_state = (n_state[0] - 2, n_state[1])
        return Windy_State(n_state)
    def moveright(self):
        n_state = (self.row, self.col+1) 
        if n_state[1] in [3,4,5,8]: 
            if n_state[0] == 0: 
                n_state = n_state
            else: 
                n_state = (n_state[0] - 1, n_state[1])
        if n_state[1] in [6,7]: 
            if n_state[0] == 0 or n_state[0]==1:
                n_state = (0, n_state[1])
            else:  
                n_state = (n_state[0] - 2, n_state[1])
        return Windy_State(n_state)
    
    
    def apply_operators(self):
        return [self.moveup(), self.movedown(), self.moveleft(), self.moveright()]
    

Search(Windy_State((3, 0)), Windy_State((3, 7)))
