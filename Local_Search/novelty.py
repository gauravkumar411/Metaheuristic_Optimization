""" Importing required Libraries """
import sys
import random
import operator
import time
import matplotlib.pyplot as plt

""" Function to check satisfiability of a solution """
def checkSatisfiability(instance, solution):
    
    noUnsatCla = 0 # Variable to count number of unsatisfied clauses
    unsatClauses = [] # list of unsatisfied clauses 
    
    for clause in instance: # Looping for each clause in the instance
            
        claSol = [] # list containing boolean value for each variable in the clause
                
        for var in clause: # Looping for each variable in the clause
                
            if int(var) in solution: # Checking if the boolean value of variable is TRUE in solution
                claSol.append(True) # Appending boolean value TRUE for the variable in claSol list
            else:
                claSol.append(False) # Appending boolean value False for the variable in claSol list
               
        if True not in claSol: # Checking if none of the variable has boolean value TRUE in the clause
            noUnsatCla += 1 # Incrementing the noUnsatCla variable by 1
            unsatClauses.append(clause) # Appending the unsatisfied clause in unsatClauses list
    
    if noUnsatCla == 0: # Checking if number of unsatisfied clauses is 0 or not for the given solution
        return True, noUnsatCla # If yes, return True and count 0
    else:
        return False, noUnsatCla, unsatClauses # If no, return False, count of unsatisfied clauses and list of unsatisfied clauses

""" Function to find best and second best variables OR random variable to flip from a random unsatisfied clause """
def bestVariableToFlipNovelty(unSatClause, sol, instance, wp):

    prob = random.uniform(0,1) # Calculating random probability between 0 and 1
    
    if prob <= wp: # Checking if the random probability is <= 0.4
        
        randVar = random.randint(0, len(unSatClause)-1) # Getting random index of the random unsatisfied clause
        return [unSatClause[randVar]] # return the selected random variable to flip
    
    else:
        
        noUnsatClau = {} # Dictionary to contain number of unsatisfied clauses for a variable after flipping it
        
        for x in unSatClause: # For each variable of unsatisfied clause

            sol[abs(int(x))-1] = sol[abs(int(x))-1] * -1 # Flip the selected variable in the copy of solution
 
            result = checkSatisfiability(instance, sol) # Check how many unsatisfied clauses are after flipping the selected variable
            
            noUnsatClau.update({x:result[1]}) # Store the variable and it's corresponding count of unsatisfied caluses in the dictionary
            sol[abs(int(x))-1] = sol[abs(int(x))-1] * -1 # Flip the selected variable back to it's original value
        
        sortedDict = sorted(noUnsatClau.items(), key=operator.itemgetter(1)) # Sort the dictionary on the basis of VALUES (count of unsatisfied clauses) 
        
        return [sortedDict[0][0],sortedDict[1][0]] # returning the best and second best variable
        
""" Function to search for the solution of given instance """
def noveltySeacrh(instance, max_iterations, wp, p, noVar):
    
    recentFlippedDict = {} # Dictionary to store best variable flipped in the clause
    sol = [] # list containg the solution of given instance
    
    """ Generating random solution for the instance """
    for var in range(1, noVar+1):
        sol.append(random.choice([var,-var]))
    
    for iteration in range(max_iterations): # Looping for the number of restarts i.e. 100000
        
        result = checkSatisfiability(instance, sol) # Checking satisfiability of the given solution
                
        if result[0] == True: # checking if the given solution is satisfying the instance
            
            return sol # if yes, return the solution
        
        randClauIndex = random.randint(0, result[1]-1) # Select a random index from the range of number of unsatisfied clauses present in result[1]
        
        randUnsatClau = result[2][randClauIndex] # Selecting random unsatisfied clause from the list of unsatisified clauses
        
        solCopy = sol.copy() # Making a copy of the given solution
        
        twoBestVarToFlip = bestVariableToFlipNovelty(randUnsatClau, solCopy, instance, wp) # Getting the best and second best variable OR random variable to flip

        if len(twoBestVarToFlip) == 1: # if the returned variable is only one i.e. random
            
            sol[abs(int(twoBestVarToFlip[0]))-1] = sol[abs(int(twoBestVarToFlip[0]))-1] * -1 # if yes, flip the random variable in the solution
            
        elif len(twoBestVarToFlip) == 2: # if the returned variables are two variables i.e. best and second best
            
            if str(randUnsatClau) in recentFlippedDict: # check if the clause is persent in recentFlippedDict
                
                if abs(int(twoBestVarToFlip[0])) != recentFlippedDict[str(randUnsatClau)]: # if yes, check if the best variable is same as the recent flipped variable of the given clause
                                                                                           # if not:
                    recentFlippedDict[str(randUnsatClau)] = abs(int(twoBestVarToFlip[0])) # update the recent flipped variable of the given clause in the dictionary
                    sol[abs(int(twoBestVarToFlip[0]))-1] = sol[abs(int(twoBestVarToFlip[0]))-1] * -1 # flip the best variable in the solution
            
                else:
                
                    prob = random.uniform(0,1) # Calculating random probability between 0 and 1
                    
                    if prob <= p: # Checking if the random probability is <= 0.3
                        
                        recentFlippedDict[str(randUnsatClau)] = abs(int(twoBestVarToFlip[1])) # update the recent flipped variable of the given clause in the dictionary
                        sol[abs(int(twoBestVarToFlip[1]))-1] = sol[abs(int(twoBestVarToFlip[1]))-1] * -1 # flip the second best variable in the solution
                    
                    else:
                        
                        recentFlippedDict[str(randUnsatClau)] = abs(int(twoBestVarToFlip[0])) # update the recent flipped variable of the given clause in the dictionary
                        sol[abs(int(twoBestVarToFlip[0]))-1] = sol[abs(int(twoBestVarToFlip[0]))-1] * -1 # flip the best variable in the solution
            else:
                
                recentFlippedDict[str(randUnsatClau)] = abs(int(twoBestVarToFlip[0])) # update the recent flipped variable of the given clause in the dictionary
                sol[abs(int(twoBestVarToFlip[0]))-1] = sol[abs(int(twoBestVarToFlip[0]))-1] * -1 # flip the best variable in the solution
            
    return "No Solution Found" # If no solution found, return "No Solution Found"
            
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print ("Error - Incorrect input")
        sys.exit(0)
    
    max_iterations = 100000 # number of maximum iterations
    wp = 0.4 # probability with which either random OR best and second best variable is selected
    p = 0.3 # probability with which either best or second best variable is selected
    
    filedir = "" # Directory of instance files

    instanceFile = sys.argv[1] # Getting name of the insatnce file from command line
    
    noVar = 0 # variable to store number of variables in instance file
    noCla = 0 # variable to store number of clauses in the instance file

    instance = [] # list to store clauses in the instance file
    
    """ Reading the instance file """
    with open(filedir+"Inst/"+instanceFile) as instFile:
        for line in instFile:        
            if (line.startswith("p")):
                noVar = int(line.split()[2])
                noCla = int(line.split()[3])
            if not (line.startswith("c") or line.startswith("p") or line.startswith("%") or (len(line)<3)):
                instance.append(line.rstrip("0\n").split())

    iterations = [] # list to store number of iterations
    times = [] # list to store time taken for the program to find a solution for the instance file
    
    for i in range(1, 101): # Looping to execute 100 iterations of tabu search
        
        iterations.append(i/100) # appending itertion number divided by 100 (total number of iterations)
        t_start = time.time() # Noting the start time of iteration
        
        sol = noveltySeacrh(instance, max_iterations, wp, p, noVar) # calling the noveltySearch function to find solution for the given instance file
        
        times.append(time.time()-t_start) # appending the tiken taken for the program to search for the solution
        print("Solution : ",sol) # printing the solution for the instance
        
    times.sort() # sorting the times list
    plt.plot(times,iterations) # plotting a graph of run-time and iterations
    plt.xlabel("run-time [CPU sec]")
    plt.ylabel("P(solve)")
    plt.title("Novelty Search for instance uf20-021.cnf")
    plt.show()