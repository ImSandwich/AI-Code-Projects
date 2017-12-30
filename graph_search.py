'''This program refers to pg. 79 Fig 3.10'''

import random
import time
import copy 
import math

class search:
    pass

class graph_search(search):

    def __init__(self):
        self.queue = []
        self.expanded = []

    def evaluate(self, input, match, heuristic=False):
        start_time = time.time()
        self.queue = [input]
        self.expanded = []
        self.expanded.append(input)

        while len(self.queue) > 0:
            terminal = self.queue.pop(0)
            print('Examining: ' + str(terminal.couplet))
            if terminal.heuristic_positional(match) == 0:
                time_elapsed = time.time() - start_time
                print("Time taken: {}".format(str(time_elapsed)))
                op=""
                while terminal is not None:
                    op += str(terminal.couplet) + "<-"
                    terminal = terminal.parent
                print(op)
                break
            for i in terminal.possible_moves():
                exists = False
                for j in self.expanded:
                    if len([k for k,l in zip(j.couplet, i.couplet) if k!=l]) is 0 and j.boat is i.boat:
                        exists = True
                if not exists:
                    self.queue.append(i)
                    self.expanded.append(i)
            
            #sort best-search queue

            print('Currentqueue: ')
            if heuristic:
                self.queue.sort(key= lambda x: x.heuristic_positional(match))
            print([str(x.couplet) for x in self.queue])
class board:
    
    def __init__(self):
        self.table = []
        self.randomize()


    def randomize(self):
        self.table = []
        numbers = ['1','2','3','4','5','6','7','8',' ']
        random.shuffle(numbers)
        for i in range(0,3):
            self.table.append([numbers[i*3 + 0],numbers[i*3 + 1],numbers[i*3 + 2]])

    def print(self):
        for i in range(0,3):
            print('{}|{}|{}'.format(self.table[i][0],self.table[i][1],self.table[i][2]))


    def possible_moves(self):
        moves = []
        spot = 0
        for i in range(0,10):
            if self.table[i//3][i%3] is ' ':
                spot = i
                break
        
        if spot % 3 is not 0:
            left = board()
            left.table = copy.deepcopy(self.table)
            left.table[spot//3][spot%3] = left.table[spot//3][spot%3 - 1]
            left.table[spot//3][spot%3 - 1] = ' '
            moves.append(left)
            
        if spot % 3 is not 2:
            right = board()
            right.table = copy.deepcopy(self.table)
            right.table[spot//3][spot%3] = right.table[spot//3][spot%3 + 1]
            right.table[spot//3][spot%3 + 1] = ' '
            moves.append(right)
            
        if spot // 3 is not 0:
            up = board()
            up.table = copy.deepcopy(self.table)
            up.table[spot//3][spot%3] = up.table[spot//3 - 1][spot%3]
            up.table[spot//3 - 1][spot%3] = ' '
            moves.append(up)
            
        if spot // 3 is not 2:
            down = board()
            down.table = copy.deepcopy(self.table)
            down.table[spot//3][spot%3] = down.table[spot//3 + 1][spot%3]
            down.table[spot//3 + 1][spot%3 ] = ' '
            moves.append(down)
            

        return moves

    def heuristic_positional(self, goal):
        cost = 0
        for row in range(0,3):
            for column in range(0,3):
                if self.table[row][column] is not goal[row][column]:
                    cost += 1
        return cost

    def victory(self, goal):
        return self.heuristic_positional(goal) is 0

class mcnode:
    def __init__(self, cp, pr):
        self.couplet = cp
        self.parent = pr
        if pr is None:
            self.boat = 1
        else:
            self.boat = 0 if pr.boat is 1 else 1
    
    def possible_moves(self):
        output = []
        #post-transitional-model
        actions = [[0,1], [0,2], [1,1], [1,0], [2,0]]
        for i in actions:
            current = copy.deepcopy(self.couplet)
            if self.boat is 1:
                current = [x-y for x,y in zip(current, i)]
            else:
                current = [x+y for x,y in zip(current, i)]
                
            #perform check
            if (current[0] == current[1] or current[0] == 3 or current[0] == 0) and (current[0] >= 0 and current[1] >= 0) and (current[0] <= 3 and current[1] <= 3):
                next_node = mcnode(current, self)
                output.append(next_node)
        return output
    def heuristic_positional(self, goal):
        cost = abs(goal[0] - self.couplet[0]) + abs(goal[1] - self.couplet[1])
        return cost

    def print(self):
        print(str(self.couplet) + ":{} ".format(str(self.boat)))

def compareListofLists(list1, list2):
    tuple_list1 = [tuple(x) for x in list1]
    tuple_list2 = [tuple(x) for x in list2]
    
    tuple_set1 = set(tuple_list1)
    tuple_set2 = set(tuple_list2)

    return len(tuple_set1 ^ tuple_set2) is 0


def main():
    print('Program initialized.')
    algorithm = graph_search()
    '''
    #8-puzzle
    new_board = board()
    new_board.table = [['1','2','3'],['7', '4', '5'], [' ', '8', '6']]
    new_board.print()
    
    victory_condition = [['1','2','3'], ['4','5','6'], ['7','8',' ']]
    print("With heuristic:")
    algorithm.evaluate(new_board, victory_condition,heuristic=True)
    algorithm.evaluate(new_board, victory_condition)
    '''   
    new_mcnode = mcnode([3,3], None)
    new_mcnode.print()

    victory_condition = [0,0]
    print("With heuristic:")
    algorithm.evaluate(new_mcnode, victory_condition, heuristic=True)
    print("Without heuristic:")
    algorithm.evaluate(new_mcnode, victory_condition, heuristic=True)

if __name__ == "__main__":
    main()