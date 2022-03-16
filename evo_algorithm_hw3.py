import statistics
import math
import random
import matplotlib.pyplot as plt

n = 8
e = .02

def dec_to_bin(number): 
    """converts integers between 0-255 into 8-bit binary lists"""
    x = []
    x.append(number//2**7)
    number = number % 2**7
    x.append(number//2**6)
    number = number % 2**6
    x.append(number//2**5)
    number = number % 2**5
    x.append(number//2**4)
    number = number % 2**4
    x.append(number//2**3)
    number = number % 2**3
    x.append(number//2**2)
    number = number % 2**2
    x.append(number//2**1)
    number = number % 2**1
    x.append(number//2**0)
    return x

def bin_to_dec(bin_list): 
    """converts 8-bit binary list into an integer""" 
    number = 0
    number+=bin_list[0]*2**7
    number+=bin_list[1]*2**6
    number+=bin_list[2]*2**5
    number+=bin_list[3]*2**4
    number+=bin_list[4]*2**3
    number+=bin_list[5]*2**2
    number+=bin_list[6]*2**1
    number+=bin_list[7]*2**0
    return number
    
def init_pop(): 
    """returns a list (length n=8) of binary encoded individuals, each 
    individual is an 8-bit binary list"""
    pop = []
    for i in range(n): 
        x=random.randint(0,256)
        pop.append(dec_to_bin(x))
    return pop 

def check_fit(pop): 
    """takes in a list of n=8 binary encoded individuals, returns a list of 8 
    floats based on each individual's fitness"""
    fitness_list = []
    for individual in pop: 
        x = bin_to_dec(individual)
        indiv_fit = math.sin((x*math.pi)/256)
        fitness_list.append(indiv_fit)
    best_fit = max(fitness_list)
    mean_fit = statistics.mean(fitness_list)
    return fitness_list, best_fit, mean_fit

def normalize_fit(fitness_list):
    """takes in a list of 8 floats and divides by the sum, returns normalized list"""
    total = sum(fitness_list)
    norm_fitness_list = []
    for i in fitness_list: 
        norm_fitness_list.append(i/total)
    return norm_fitness_list

def pick_fittest(norm_fitness_list, pop): 
    """returns the 8 fittest individuals (with repetition, and some randomization)
    from a normalized population of 8 individuals"""
    fittest = []
    fit_pop = []
    for i in range(n): 
        r = random.random()
        ind = norm_fitness_list.index(norm_fitness_list[min(range(len(norm_fitness_list)), 
                              key = lambda i: abs(norm_fitness_list[i]-r))])
        fit_pop.append(pop[ind])
        fittest.append(norm_fitness_list[ind])
    return fit_pop, fittest

def crossover(fit_pop):
    """creates four pairs from 8 parents and generates and returns 8 children"""
    random.shuffle(fit_pop)
    children_pop = []
    for i in range(0,8,2): 
        k = random.choice(range(0, 8))
        head1 = fit_pop[i][0:k]
        tail1 = fit_pop[i][k:8]
        head2 = fit_pop[i+1][0:k]
        tail2 = fit_pop[i+1][k:8]
        kid1 = head1+ tail2
        kid2 = head2+tail1
        children_pop.append(kid1)
        children_pop.append(kid2) 
    return children_pop

def mutate(children_pop): 
    """takes each of the 8 bits in each of the 8 individuals in the population
    and with probability e = .02 flips the bit from 0 to 1 or from 1 to 0"""
    for child in children_pop: 
        for i in range(0,8): 
            r = random.random()
            if r<e: 
                child[i] = (child[i]+1)%2
    return children_pop

def e_a_iteration(): 
    """combines all the other functions to iterate through our evolutionary 
    algorithm until the average fit of our population is higher than .9999 or until 
    it reaches 10,000 generations."""
    
    pop = init_pop() 
    iters = 0 
    iters_lst = []
    best_fit = 0 
    mean_fit = 0 
    lst_best_fit = []
    lst_mean_fit = []
    while iters < 10000 and mean_fit < .9999: 
        fitness_list, best_fit, mean_fit = check_fit(pop) 
        lst_best_fit.append(best_fit)
        lst_mean_fit.append(mean_fit) 
        norm_fitness_list = normalize_fit(fitness_list)
        fit_pop, fittest = pick_fittest(norm_fitness_list, pop)
        children_pop = crossover(fit_pop)
        mutated_pop = mutate(children_pop)
        pop = mutated_pop 
        iters_lst.append(iters)
        iters +=1
        #print(best_fit) 
    return lst_best_fit, lst_mean_fit, iters_lst

lst_best_fit, lst_mean_fit, iters_lst = e_a_iteration()

plt.plot(lst_best_fit, iters_lst)
plt.plot(lst_mean_fit, iters_lst)
plt.xlabel('Fitness')
plt.ylabel('Number of Generations')
plt.legend(['best fitness', 'mean fitness'])
