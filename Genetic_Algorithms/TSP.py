import random
from Individual import Individual
import sys
import time

class BasicTSP:
    def __init__(self, _fName, _popSize, _mutationRate, _maxIterations):
        """
        Parameters and general variables
        """

        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = _popSize
        self.genSize        = None
        self.mutationRate   = _mutationRate
        self.maxIterations  = _maxIterations
        self.iteration      = 0
        self.fName          = _fName
        self.data           = {}

        self.readInstance()
        self.initPopulation()


    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (id, x, y) = line.split()
            self.data[int(id)] = (int(x), int(y))
        file.close()

    def initPopulation(self):
        """
        Creating random individuals in the population
        """
        for i in range(0, self.popSize):
            individual = Individual(self.genSize, self.data)
            individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        print ("Best initial sol: ",self.best.getFitness())

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
            print ("Iteration:",self.iteration, " Best: ",self.best.getFitness())

    def randomSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[ random.randint(0, self.popSize-1) ]
        indB = self.matingPool[ random.randint(0, self.popSize-1) ]
        return [indA, indB]
    
    def bestAndSecondBest(self):
    
        twoBestInd = []
    
        #Index = []
        while len(twoBestInd) < 2:
           
            maxFitness = self.matingPool[0].getFitness()
            for i in range(0, self.popSize-1):
                 if self.matingPool[i] not in twoBestInd:
                    if (self.matingPool[i].getFitness()) < maxFitness:
                        maxFitness = self.matingPool[i].getFitness()        
            
            for j in range(0, self.popSize-1):
                if self.matingPool[j] not in twoBestInd:
                    if (self.matingPool[j].getFitness()) == maxFitness:
                        twoBestInd.append(self.matingPool[j])
            
        return twoBestInd
                         

    def rouletteWheel(self):
        """
        Your Roulette Wheel Selection Implementation
        """
        sum = 0
        r = random.random()
        parents = []
        sum_prob = 0
        
        for i in range(0, self.popSize-1):
            sum += self.matingPool[i].getFitness()
        
        for i in range(0, self.popSize-1):
            sum_prob += (self.matingPool[i].getFitness()/sum)
            if r < sum_prob:
                while len(parents) < 2:
                    parents.append(self.matingPool[i])
            if len(parents) == 2:
                break
            
        return parents
 
    def uniformCrossover(self, indA, indB):
        """
        Your Uniform Crossover Implementation
        """        
        child = indA.genes.copy()
        indexes = []
        
        for i in range(0, self.genSize):
            indexes.append(random.randint(0,1))

        index = []
        value = []
        
        for i in range(0, self.genSize):
            if indexes[i] == 0:
                child[i] = None
                index.append(i)
        
        for i in range(0, self.genSize):
            if indB.genes[i] not in child:
                value.append(indB.genes[i])

        for i in range(0, len(value)):
            child[index[i]] = value[i]
          
        return child

    def cycleCrossover(self, indA, indB):
        """
        Your Cycle Crossover Implementation
        """
        loopCounter = 0
        loops = []
        indexes = []
        child = indA.genes.copy()
        #ind = []
        
        for i in range(len(indA.genes)):
            indexes.append(None)
        
        for i in range(len(indA.genes)):
            if indA.genes[i] not in loops:
                #ind.append(i)
                j = i
                while j < len(indB.genes):
                    if indB.genes[j] not in loops:
                        loops.append(indA.genes[i])
                        #ind.append(A.index(B[j]))
                        indexes[i] = loopCounter + 1
                        indexes[indA.genes.index(indB.genes[j])] = loopCounter + 1
                        loops.append(indB.genes[j])
                        j = indA.genes.index(indB.genes[j])
                    elif indB.genes[j] in loops:
                        break
                loopCounter += 1
            if indA.genes in loops:
                break
        
        for i in range(len(indA.genes)):
            if indexes[i] % 2 == 0:
                child[i] = indB.genes[i]
            else:
                child[i] = indA.genes[i]
        return child
    
    def reciprocalExchangeMutation(self, ind):
        """
        Your Reciprocal Exchange Mutation implementation
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

        ind.computeFitness()
        self.updateBest(ind)
        """
        indexA = random.randint(1, int(self.genSize/2))
        indexB = random.randint(1, int(self.genSize/2))
        
        indexC = random.randint(int(self.genSize/2)+1, self.genSize-1)
        indexD = random.randint(int(self.genSize/2)+1, self.genSize-1)
        
        #to make sure indexA < index B and indexC < indexD
        while((indexA >= indexB) or (indexC >= indexD)):
            indexA = random.randint(1, int(self.genSize/2))
            indexB = random.randint(1, int(self.genSize/2))
            indexC = random.randint(int(self.genSize/2)+1, self.genSize-1)
            indexD = random.randint(int(self.genSize/2)+1, self.genSize-1)
    
        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp
    
        tmp = ind.genes[indexC]
        ind.genes[indexC] = ind.genes[indexD]
        ind.genes[indexD] = tmp
        
        ind.computeFitness()
        self.updateBest(ind)
        """
    def scrambleMutation(self, ind):
        """
        Your Scramble Mutation implementation
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)
        
        #to make sure indexA < indexB
        while((indexA >= indexB) or (indexB-indexA <= 1)):
            indexA = random.randint(0, self.genSize-1)
            indexB = random.randint(0, self.genSize-1)
        
        for i in range(10):
            i1 = random.randint(indexA, indexB)
            i2 = random.randint(indexA, indexB)
            temp = ind.genes[i1]
            ind.genes[i1] = ind.genes[i2]
            ind.genes[i2] = temp
        
        ind.computeFitness()
        self.updateBest(ind)

    def crossover(self, indA, indB):
        """
        Executes a 1 order crossover and returns a new individual
        """
        child = []
        tmp = {}

        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        for i in range(0, self.genSize):
            if i >= min(indexA, indexB) and i <= max(indexA, indexB):
                tmp[indA.genes[i]] = False
            else:
                tmp[indA.genes[i]] = True
        aux = []
        for i in range(0, self.genSize):
            if not tmp[indB.genes[i]]:
                child.append(indB.genes[i])
            else:
                aux.append(indB.genes[i])
        child += aux
        return child

    def mutation(self, ind):
        """
        Mutate an individual by swaping two cities with certain probability (i.e., mutation rate)
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

        ind.computeFitness()
        self.updateBest(ind)

    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation
        """
        self.matingPool = []
        for ind_i in self.population:
            self.matingPool.append( ind_i.copy() )

    def newGeneration(self, configuration):
        """
        Creating a new generation
        1. Selection
        2. Crossover
        3. Mutation
        """
        if configuration == 1:
            for i in range(0, len(self.population)):
                [ind1, ind2] = self.randomSelection()
                child = self.uniformCrossover(ind1,ind2)
                self.population[i].setGene(child)
                self.reciprocalExchangeMutation(self.population[i])
        
        if configuration == 2:
            for i in range(0, len(self.population)):
                [ind1, ind2] = self.randomSelection()
                child = self.cycleCrossover(ind1,ind2)
                self.population[i].setGene(child)
                self.scrambleMutation(self.population[i])
                
        if configuration == 3:
            for i in range(0, len(self.population)):
                [ind1, ind2] = self.rouletteWheel()
                child = self.uniformCrossover(ind1,ind2)
                self.population[i].setGene(child)
                self.reciprocalExchangeMutation(self.population[i])

        if configuration == 4:
            for i in range(0, len(self.population)):
                [ind1, ind2] = self.rouletteWheel()
                child = self.cycleCrossover(ind1,ind2)
                self.population[i].setGene(child)
                self.reciprocalExchangeMutation(self.population[i])
                
        if configuration == 5:
            for i in range(0, len(self.population)):
                [ind1, ind2] = self.rouletteWheel()
                child = self.cycleCrossover(ind1,ind2)
                self.population[i].setGene(child)
                self.scrambleMutation(self.population[i])
                
        if configuration == 6:
            for i in range(0, len(self.population)):
                [ind1, ind2] = self.bestAndSecondBest()
                child = self.uniformCrossover(ind1,ind2)
                self.population[i].setGene(child)
                self.scrambleMutation(self.population[i])
                
    def GAStep(self, config):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """

        self.updateMatingPool()
        self.newGeneration(config)

    def search(self, config):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep(config)
            self.iteration += 1

        print ("Total iterations: ",self.iteration)
        print ("Best Solution: ", self.best.getFitness())

if len(sys.argv) == 1:
    files = ["inst-0.tsp","inst-13.tsp","inst-16.tsp"]
    for problem_file in files:
        for configuration in (1,7):
            for i in range(1,4): #run test 3 times
                startTime = time.time()
                ga = BasicTSP(problem_file, 100, 0.1, 300)
                ga.search(configuration)
                endTime = (time.time() - startTime)/60
                print("problem_file:",problem_file,", configuration:",configuration, "test number:", i, "time taken:",endTime," minutes")
                del ga
    sys.exit(0)
