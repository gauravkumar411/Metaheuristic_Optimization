""" Importing required Libraries """
import sys
import math
import random
import time
import operator

data = {} # global dictionary to store the city and it's co-ordinates

""" Function to read the instance of TSP """
def loadInstance(instanceDir, instanceFile):
    
    file = open(instanceDir+instanceFile, 'r') # Opening the instance file
    noOfCities = int(file.readline()) # Getting the number of cities in the instance file
    
    global data # using the global dictionary
    data = {}
    
    for line in file: # looping for each line in the instance file
        (id, x, y) = line.split() # splitting each line into id, x, y
        data[int(id)] = (int(x), int(y)) # storing city and it's co-ordinates in data dictionary
    file.close() # closing the file
    return (noOfCities,data) # return number of cities in the instance file and data dictionary

""" Function to generate the initial solution of instance """
def generateSolution(tour):
    
    if tour == "random": # if the initial solution to be generated is random
        
        print("Random Solution")
        
        solution = [] # list to store random solution
    
        solution = random.sample(data.keys(), noOfCities) # Generating random solution
    
        return solution # returning random solution
    
    elif tour == "nearest_neighbour": # if the initial solution to be generated is nearest neighbour
        
        print("Nearest Neighbour Solution")
        
        unvisitedCities = list(data.keys()).copy() # Creating copy of list of cities of instance file as unvisited cities
        visitedCities = [] # list to store visited cities
        
        index = random.randint(0, len(unvisitedCities)) # selecting random index to select random city
        
        start = unvisitedCities[index] # selecting random city to start the tour
        visitedCities.append(start) # appending the starting city in visitedCities list
        unvisitedCities.pop(index) # removing starting city from unvisitedCities list
        
        while len(unvisitedCities) > 0: # loop till every city is visited
            
            distances = {} # dictionary to store distance between currect city and rest of the cities
            
            for x in range(0, len(unvisitedCities)): # Looping for the number of unvisited cities
                
                distances[unvisitedCities[x]] = euclideanDistance(start, unvisitedCities[x]) # calculating distance between currect city and the given city
            
            c = min(distances.items(), key=operator.itemgetter(1))[0] # finding the city nearest to the currect city
            visitedCities.append(c) # appending the nearest city in the visitedCities list
            unvisitedCities.pop(unvisitedCities.index(c)) # removing the nearest city from the unvisitedCities list
            distances = {} # 
            start = c # making the nearest city as the currect city
        
        return visitedCities # return the nearest neighbour solution
    
""" Function to find euclidean distance between the given two cities """
def euclideanDistance(c1, c2):

    d1 = data[c1] # Getting co-ordinates for first city      
    d2 = data[c2] # Getting co-ordinates for second city
        
    return math.sqrt((d1[0]-d2[0])**2 + (d1[1]-d2[1])**2) # return euclidean distance between given two cities

""" Function to compute the fitness of the solution """
def computeFitness(listOfCities, noOfCities):
 
    fitness = euclideanDistance(listOfCities[0], listOfCities[len(listOfCities)-1])
    for i in range(0, noOfCities-1):
        fitness += euclideanDistance(listOfCities[i], listOfCities[i+1])
    return fitness

""" Function to find the best 3-opt combination """
def localSearch(solution, cost):
    
    sol = [] # list to store solution
    ct = 0 # variable to store the cost of sol

    a = random.randint(0, len(solution)) # Getting one random edge from the currect tour
    
    for b in range(0, len(solution)): # Looping for the length of solution to find second edge
        if b == a: # check if the second edge is same as first random edge
            continue # if yes, continue and find different second edge
        
        c = b+1 # Initializing the third edge to be second edge + 1
        while c < len(solution): # Looping till the last edge of the tour
            if c == a or c == b: # check if the third edge is same as first or second edge
                c += 1 # increment the third edge by 1
                continue # continue
            
            a, b, c = sorted([a, b, c]) # sort all the three edges
            
            """ Finding the best combination of 3 edges from the 7 possible combinations below """
            """ If a better solution is found, update the currect solution """
            sol = solution[:a+1] + solution[b+1:c+1] + solution[a+1:b+1] + solution[c+1:] #1
        
            ct = computeFitness(sol, noOfCities)
             
            if ct < cost:
                
                solution = sol
                cost = ct
            
            sol = solution[:a+1] + solution[c:b:-1] + solution[a+1:b+1] + solution[c+1:] #2
            
            ct = computeFitness(sol, noOfCities)
            
            if ct < cost:
                
                solution = sol
                cost = ct
                
            sol = solution[:a+1] + solution[b:a:-1] + solution[c:b:-1] + solution[c+1:] #3
            
            ct = computeFitness(sol, noOfCities)
            
            if ct < cost:
                
                solution = sol
                cost = ct 
            
            sol = solution[:a+1] + solution[b+1:c+1] + solution[b:a:-1] + solution[c+1:] #4
            
            ct = computeFitness(sol, noOfCities)
            
            if ct < cost:
                
                solution = sol
                cost = ct
        
            sol = solution[:a+1] + solution[b:a:-1] + solution[b+1:c+1] + solution[c+1:] #5
            
            ct = computeFitness(sol, noOfCities)
            
            if ct < cost:
                
                solution = sol
                cost = ct
                
            sol = solution[:a+1] + solution[a+1:b+1] + solution[c:b:-1] + solution[c+1:] #6
            
            ct = computeFitness(sol, noOfCities)
            
            if ct < cost:
                
                solution = sol
                cost = ct
                
            sol = solution[:a+1] + solution[c:b:-1] + solution[b:a:-1] + solution[c+1:] #7
            
            ct = computeFitness(sol, noOfCities)
            
            if ct < cost:
                
                solution = sol
                cost = ct
            
            c += 1 # Incrementing the third edge by 1
            
    return solution, cost #  returning the best solution and it's cost (fitness)

""" Function to find the best 2-opt combination """
def perturbation(solution, cost):

    sol = [] # list to store solution
    ct = 0 # variable to store the cost of sol
    
    for x in range(0, 5): # Looping for 5 times to find best 2-opt solution
    
        i, j = random.sample(range(len(solution) + 1), 2) # Getting two random edges from the currect tour
        i, j = sorted([i,j]) # sort both the edges
        
        """ Finding the best combination of 2 edges from the 1 possible combination below """
        """ If a better solution is found, update the currect solution """
        sol = solution[:i+1] + solution[j:i:-1] + solution[j+1:] 
        
        ct = computeFitness(sol, noOfCities)
        
        if ct < cost:
        
            solution = sol
            cost = ct
            
    return solution, cost #  returning the best solution and it's cost (fitness)

""" Function to decide whether to update solL(s*) or not """
def acceptanceCriterion(solL, ctL, solLo, ctLo):
    
    number = random.choice(random.sample(range(1, 21), 20))# finding the random probaility for 1 to 20
    #if we get number == 1, it's probability is 1/20 = 0.05 i.e. 5%
    #if we get number == 10, it;s probability is 10/20 = 0.5 i.e. 50%
    
    if number == 1: # having probability = 5%
        return solLo, ctLo # return the solLo(s'*) solution as the chosen solution
    else:
        if ctL < ctLo: # find the solution with lowest cost(fitness)
            return solL, ctL # return solL(s*) as the chosen solution
        else:
            return solLo, ctLo # return solLo(s'*) as the chosen solution
        
if __name__ == "__main__":
    
    if len(sys.argv) < 1:
        print ("Error - Incorrect input")
        sys.exit(0)
        
    instanceFiles = ["inst-0.tsp",'inst-13.tsp'] # instance files
    
    instanceDir = "" # Directory of instance files
    
    choice = ("random","nearest_neighbour") # tuple to choose which initial solution to be generated
    
    for file in instanceFiles: # for each file in instanceFiles list
        
        noOfCities, data = loadInstance(instanceDir, file) # load the given instance file
        listOfCities = list(data.keys()) # Getting the list of cities from the insatnce file
        
        for s in range(0, 2): # looping for each choice of initial solution generation
            
            solution = generateSolution(choice[s]) # generating the initial solution either random or nearest neighbour
        
            for iteration in range(0, 5): # Looping for 5 times for each instance file
            
                print("Iteration for ",choice[s]," and instance ", file, "number", iteration)
                cost = computeFitness(solution, noOfCities) # Compute cost(fitness) of the initial solution
                print("Original Cost : ",cost)
                solL, ctL = localSearch(solution, cost) # Calling localSearch function to find the best route
                
                t_end = time.time() + 60 * 5 # setting time for the while loop to run for 5 minutes
           
                while time.time() < t_end: # running while loop for 5 minutes
                
                    solP, ctP = perturbation(solL, ctL) # Finding the best 2-opt solution for the given solution
                    solLo, ctLo = localSearch(solP, ctP) # Finding the best 3-opt solution for the given solution
                    solL, ctL = acceptanceCriterion(solL, ctL, solLo, ctLo) # Choosing the best solution out of solL(s*) and solLo(s'*)
            
                solution = solL # updating the currect solution with the best solution
                cost = ctL # updating the currecnt cost(fitness) with the best cost(fitness)
                print("Updated Cost", cost) # Printing the best cost