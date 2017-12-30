import random
import copy
import math
import statistics

class genetic_algorithm:
    def __init__(self, size, mutation, cutoff, scatter):
        self.mutation = mutation
        self.plateau = []
        self.population = []
        self.cutoff = cutoff
        self.scatter = scatter
        self.pop_size = size

    def initialize(self, sample):
        while len(self.population) < self.pop_size:
            candidate = sample.random()
            if candidate.fitness() >= self.cutoff:
                self.population.append(candidate)

    def crossover_population(self):
        offspring_population = []
        while len(offspring_population) < self.pop_size:
            candidate = self.reproduce()
            if candidate.fitness() >= self.cutoff:
                offspring_population.append(candidate)
        self.population = offspring_population
        self.plateau.append(self.population_fitness())
        if len(self.plateau) > 5:
            self.plateau.pop(0)

    def population_fitness(self):
        sum_fitness = 0
        for i in self.population:
            sum_fitness += i.fitness()
        return sum_fitness/len(self.population)

    def best_fitness(self):
        return sorted(self.population, key=lambda x: x.fitness() ,reverse=True )[0].fitness()

    def reproduce(self):
      
        
        #pick mate1
        mate1 = None
        mate2 = None
        
        self.cutoff = min([x.fitness() for x in self.population]) 
        mate1population = copy.deepcopy(self.population)
        for i in range(len(mate1population)- 1, -1, -1):
            if mate1population[i].fitness() < self.cutoff:
                mate1population.remove(mate1population[i])
        
        elite_population = sorted(mate1population, key=lambda x: x.fitness(), reverse=False)
        
        aggregate_score = 0
        for i in range(0, len(elite_population)):
            aggregate_score += i + 1
        score_pointer = 0
        pointter_loc = random.uniform(0, aggregate_score)
        
        for i in range(0, len(elite_population)):
            score_pointer += i+1
            if score_pointer >= pointter_loc:
                mate1 = elite_population[i]
                elite_population.remove(elite_population[i])
                break
        
       
        #EXCEPTION IF MATE1 is not chosen
        if mate1 is None: 
            print("MATE1 not chosen")

        aggregate_score = 0
        for i in range(0, len(elite_population)):
            aggregate_score += i + 1
        score_pointer = 0
        pointter_loc = random.uniform(0, aggregate_score)
        

        for i in range(0, len(elite_population)):
            score_pointer += i+1
            if score_pointer >= pointter_loc:
                mate2 = elite_population[i]
                break
        
        #EXCEPTION IF MATE2 is not chosen
        if mate2 is None: 
            print("MATE2 not chosen")
    
    #
  

        split_loc = random.random()
        offspring = mate1.join(mate2, split_loc)
        for k in offspring.variable:
            if random.uniform(0,1) < self.mutation:
                k[2] = random.randrange(1,len(mate1.table)+1)
            
        offspring.apply_variable()
        return offspring

    def print_population(self):
        for r in range(0,len(self.population[0].table)):
            line = ""
            for p in range(0, len(self.population)):
                if p != 0:
                    line += " | "
                line+= str(self.population[p].table[r])
            print(line)
    
    def print_best(self):
        best = max(self.population,key=lambda x: x.fitness())
        best.print()

class sudoku:

    def __init__(self, table):
        self.sampletable = table
        self.variable = [] #list of triplets: X,Y,val
        self.table = copy.deepcopy(self.sampletable)
        for y in range(0, len(self.table)):
            for x in range(0, len(self.table[y])):
                if self.sampletable[y][x] == 0:
                    r = random.randrange(1,len(self.table)+ 1)
                    self.variable.append([y,x,r])
        self.apply_variable()

    def random(self):
        return sudoku(self.sampletable)

    def scatter(self, scatter_rate):
        for i in self.variable:
            if random.random() < scatter_rate:
                i[2] = random.randrange(1, len(self.table)+1)
        self.apply_variable()

    def fitness(self):
        fitness = 0
        for y in range(0, len(self.table)):
            for x in range(0, len(self.table[y])):
                val = int(self.table[y][x])
                #compare horizontal
                for h in range(0, len(self.table[y])):
                    if h is not x:
                        if int(self.table[y][h]) is val:
                            fitness += 1
                #compare vertical
                for v in range(0, len(self.table)):
                    if v is not y:
                        if int(self.table[v][x]) is val:
                            fitness += 1
                #compare square
                square_length = int(math.sqrt(len(self.table)))
                square = [math.floor(x/square_length), math.floor(y/square_length)]
                conflict = False
                for p in range(square_length):
                    for q in range(square_length):
                        loc = [square[0]*square_length + p, square[1]*square_length + q]
                        if loc[0] is not x or loc[1] is not y:
                            if int(self.table[loc[0]][loc[1]]) is val:
                                conflict = True
                if conflict:
                    fitness += 1
        fitness = 3 * len(self.table) * len(self.table) - fitness
        return fitness

    def apply_variable(self):
        self.table = copy.deepcopy(self.sampletable)
        for i in self.variable:
            self.table[i[0]][i[1]] = i[2]

    def split(self, degree, back=False):
        cut = int(len(self.variable) * degree)
        if back is False:
            return self.variable[:cut]
        else:
            return self.variable[cut:]
            
    def join(self, target, degree):
        joined_var = copy.deepcopy(self.split(degree))
        joined_var.extend(target.split(degree, back=True))
        combined_sudoku = sudoku(self.sampletable)
        combined_sudoku.variable = joined_var
        combined_sudoku.apply_variable()
        return combined_sudoku 

    def print(self):
        for row in self.table:
            print(row)

temperature = 0.5
def plateau_detector(meter):
    global temperature
    return statistics.stdev(meter) < temperature
    

def main():
    sample_table = [
        [0,0,0,4,0,1,0,0,6],
        [8,5,0,2,0,0,4,0,0],
        [0,2,0,5,0,0,0,0,0],
        [0,0,0,0,0,0,5,0,5],
        [4,1,0,0,0,0,0,6,3],
        [9,0,5,0,0,0,0,0,0],
        [0,0,0,0,0,8,0,2,0],
        [0,0,9,0,0,4,0,7,5],
        [7,0,0,6,0,2,0,0,0]]
    sample_sudoku = sudoku(sample_table)
    print("Starting with: ")
    sample_sudoku.print()
    user_size = int(input("Population size: "))
    user_mutation = float(input("Mutation rate [0-1]: "))
    user_cutoff = int(input("Cutoff: "))
    user_scatter = float(input("Scatter rate: "))
    algorithm = genetic_algorithm(user_size, user_mutation, user_cutoff, user_scatter)
    algorithm.initialize(sample_sudoku)
    user_input = ""
    while user_input is not "exit":
        print('-'*80)
        algorithm.print_best()
        algorithm.crossover_population()
        print("Average Fitness:{} > ".format(str(algorithm.population_fitness())))
        print("Best Fitness:{} > ".format(str(algorithm.best_fitness())))
        
        if len(algorithm.plateau) == 5:
            if plateau_detector(algorithm.plateau):
                print("SCATTER!")
                global temperature
                temperature *= 0.8
                for i in algorithm.population:
                    i.scatter(algorithm.scatter)

if __name__ == "__main__":
    main()