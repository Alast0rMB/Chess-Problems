import random

#All possilbe knight movements:
#[(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]


#Generates fenotip based on genotip
def generate_fenotip(pop):
    print(pop)
    fenotip = ""
    for i in range(size):
        for j in range(size):
            index = i*size+j
            if index in pop:
                fenotip += " K "
            else:
                fenotip += " _ "
        fenotip += "\n"
    print(fenotip)


#Finding first larger index than what we want
def find_greater(l,t):
    notfound = len(l)
    for i in range(len(l)):
        if l[i] > t:
            return i
    return notfound 

#Calculates the fitness of a genome
def fitness(genome,size):
    conflict = 0
    move_vector = [(1,2),(1,-2),(2,1),(2,-1)] #Only checking one side of the conflict
    for index in genome:
        row = int(index/size)
        col = index%size
        for x,y in move_vector:
            newrow = x + row
            newcol = y + col
            if newrow >= size or newrow < 0 or newcol >= size or newcol < 0:
                continue #invalid movement, check next
            if newrow * size + newcol in genome: #Check if there is a pair conflict
                conflict += 1
    #Calculate fitness based on size and conflict:
    knights = len(genome) #number of knights on the board is the same as genome length
    if conflict == 0:
        fitness = (size*size/2) + knights #We like the situations without conflict, bias?!
    else:
        fitness = knights/conflict #We want more nights that have less conflict 
    return fitness

#Creates a random board with knight_count knights on it
def create_random_gene(knight_count,size):
    genome = []
    for i in range(knight_count):
        #Checking if we already have the desired 
        while(True):
            index = random.randint(0, size*size-1) #create random index
            if not index in genome:
                genome.append(index)
                break
    #Get fitness function for each genome        
    genome.sort() #We sort the answer for ease on future operations
    return genome

#Creates the initial population randomly
def initial_population(size,pop_count):
    population = []
    for p in range(pop_count):
        #Creating random population:
        knight_count = random.randint(1, int(size*size/2)) #Number of knights on the board
        genome = create_random_gene(knight_count,size)  
        pop = genome.copy() #Creating a pop based one the genmoe 
        pop.append(fitness(genome, size)) #Add it's fitness 
        population.append(pop) #Add pop to the population pool
    return population

#Cross Over - using single point crossover on the row
def crossover(p1,p2,size):
    while True:
        row = random.randint(0, size-2) #Getting the row we want to use as cross point
        cross_point = row*size+size-1 #Square that we want to cut from
        #Index shows what point in the list the cross over must start
        index1 = find_greater(p1, cross_point)
        index2 = find_greater(p2, cross_point)
        #Adding the top half from one parent
        child = p1[:index1]
        #Adding the bottom half from the otherone
        child.extend(p2[index2:])
        
        if not child == []: #We don't want to return empty board
            return child

#Reproduction selection - Stochastic universal sampling
def SUS(population,size):
    total_fitness = 0 #total fitness of the group
    fitness_scale = [] #A scale that represents our wheel
    for pop in population:
        total_fitness += pop[-1] #Last item in the list is the fitness of a genome
        fitness_scale.append(total_fitness) #Setting our boundries

    selection_pool = []        
    pointer_scale = total_fitness/size #Each step the pointer has to move
    start = random.uniform(0, pointer_scale) #Selects our starting point
    
    pointers = [] #Pointers for selecting
    for i in range(size):
        pointers.append(start + i*pointer_scale)

    #RWS selection part
    fitness_pointer = 0 #The pointer that we are checking right now
    for pointer in pointers:
        while fitness_scale[fitness_pointer] < pointer: #move in the wheel
            fitness_pointer += 1 #if it's not in this section then we move to the next section
        selection_pool.append(population[fitness_pointer])
    return selection_pool

#Creating new generation
def reproduction(size,parent_pool,mutation_rate):
    new_generation = []
    while(len(parent_pool) > 0):
        #Chose parents and remove them from the pool
        parent1 = random.choice(parent_pool)
        parent_pool.remove(parent1)
        parent2 = random.choice(parent_pool)
        parent_pool.remove(parent2)
        #Create child
        child = crossover(parent1[:len(parent1)-1], parent2[:len(parent2)-1], size)
        #Check for mutation
        if random.uniform(0, 1) < mutation_rate: #Mutation must happen
            k = random.randint(0, int(size*size/2)) #Number of knights to be changed
            for knight in range(k):
                knight = random.randint(0, size*size-1) #Random location on the board   
                if knight in child:
                    child.remove(knight)
                else:
                    child.append(knight)
        child.append(fitness(child, size)) #Calculate fitness
        new_generation.append(child)
    return new_generation

#Genetic algorithm steps
def genetic_algorithm(size,pop_count,parent_count,mutation_rate,step_count):
    #Creating inital population at randim
    population = initial_population(size, pop_count)
    #Doing evelution step 
    for step in range(step_count):
        parent_pool = SUS(population, parent_count) #Chose parent pool
        new_generation = reproduction(size, parent_pool, mutation_rate) #Create new generation
        population.extend(new_generation) #Add generation to population 
        population = SUS(population, pop_count) #Select random population
        #Checking for other termination reasons
        # -- Domination
        # -- Lack of resualts
        print("Population step " + str(step) + ":")
        print(population)
    return population

#Problem parameters
size = 4 #Size of the board
pop_count = 500 #Number of population pool
parent_count = 20 #Number of parents each selection
mutation_rate = 0.02 
step_count = 20

answers = genetic_algorithm(size, pop_count, parent_count, mutation_rate, step_count)

print("Final population:")
print(answers)


