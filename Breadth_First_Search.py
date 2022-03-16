#Problem Statement: create a breadth-first search algorithm that can be used on various tree-style problems


visited_states = {}


class Queue: 
    def __init__(self):
        self.queue = []
    def enqueue(self, node):
        self.queue.append(node)
    def dequeue(self):
        if not self.empty():
            return self.queue.pop(0)
        else:
            print('Error: popping from empty queue')
            #'pop' means removing from a list, this function removes the first element
    def empty(self):
        return len(self.queue) == 0
    def __str__(self):
        q_string = 'Queue contains' + str(len(self.queue)) + 'items.\n'
        for item in self.queue:
            q_string += str(item) +'\n'
        return q_string
        
class Node:
    def __init__(self, state, parent, operator, depth):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth
    def __str__(self):
        node_string = 'State:' + str(self.state) + ' ' 
        node_string += 'Depth:' + str(self.depth) + ' ' 
        if self.parent != None: 
            node_string += 'Parent:' + str(self.parent.state) + ' '
            node_string += 'Operator:' + str(self.operator)
        return node_string
    def repeated_state(self):
        global visited_states
        if str(self.state) in visited_states:
            return True
        else:
            visited_states[str(self.state)] = True
            return False
    

class Search: 
    def __init__(self, initial_state, goal_state):
        self.clear_visited_states()
        self.q =Queue()
        self.q.enqueue(Node(initial_state, None, None, 0))
        self.goal_state = goal_state
        solution = self.execute()
        if solution == None: 
            print("search failed.")
        else: 
            self.show_path(solution)
    def clear_visited_states(self):
        global visited_states
        visited_states = {}
    def execute(self): 
        while not self.q.empty(): 
            current = self.q.dequeue()
            if self.goal_state.equals(current.state):
                return current 
            else:
                successors = current.state.apply_operators()
                operators = current.state.operator_names()
                for i, state in enumerate(successors):  
                    if not state.illegal():
                        n = Node(state, current, operators[i], current.depth + 1)
                        if n.repeated_state():
                            del(n)
                        else: 
                            self.q.enqueue(n)
                            print("entering " + str(n))
        return None
    def show_path(self, node):
        path = self.build_path(node)
        for current in path: 
            if current.depth != 0: 
                print('Operator: ', current.operator)
            print(current.state)
        print('Goal reached in ', current.depth, 'steps')
    def build_path(self, node): 
        result = []
        while node != None: 
            result.insert(0, node)
            node = node.parent
        return result
    
class Problem_State: #These 4 functions depend on the actual problem in hand 
    def illegal(self): 
        abstract()
    def apply_operators(self): 
        abstract()
    def operator_names(self): 
        abstract()
    def equals(self,state): 
        abstract()
        
