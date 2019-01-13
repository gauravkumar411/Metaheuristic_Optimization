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

""" Function to select the best varibale to flip from a random unsatisfied clause """
def bestVariableToFlip(unSatClause, sol, instance, wp, tabuList):
    
    prob = random.uniform(0,1) # Calculating random probability between 0 and 1
    
    if prob <= wp: # Checking if the random probability is <= 0.3
        
        randClause = unSatClause.copy() # Making a copy of random unsatisfied clause
        
        for i in range(0, len(unSatClause)): # For loop to find random variable not present in tabu list
            
            randVar = random.randint(0, len(randClause)-1) # Getting random index of the random unsatisfied clause
            
            if abs(int(randClause[randVar])) not in tabuList: # Checking if the random variable is present in tabu list or not
                
                return abs(int(randClause[randVar])) # If not, return the selected random variable to flip
            
            else:
                
                randClause.pop(randVar) # If yes, delete that random variable from the copy of random unsatisfied clause and search for another random variable from the copy of unsatisfied clause
        
        return "3varTABU" # If all the 3 variables are present in tabu list, return 3varTABU
                
    else: # if the probability is > 0.3
        
        noUnsatClauDict = {} # Dictionary to contain number of unsatisfied clauses for a variable after flipping it
        
        for x in unSatClause: # For each variable of unsatisfied clause

            sol[abs(int(x))-1] = sol[abs(int(x))-1] * -1 # Flip the selected variable in the copy of solution
 
            result = checkSatisfiability(instance, sol) # Check how many unsatisfied clauses are after flipping the selected variable
            
            noUnsatClauDict.update({x:result[1]}) # Store the variable and it's corresponding count of unsatisfied caluses in the dictionary
            sol[abs(int(x))-1] = sol[abs(int(x))-1] * -1 # Flip the selected variable back to it's original value
        
        sortedDict = sorted(noUnsatClauDict.items(), key=operator.itemgetter(1)) # Sort the dictionary on the basis of VALUES (count of unsatisfied clauses) 
        
        for x in range(0, len(unSatClause)): # Looping to find the best variable to flip that is not in tabu list
            
            if abs(int(sortedDict[x][0])) not in tabuList: # Checking if the selected variable from the sorted list of tuples is present in tabu list or not
            
                return abs(int(sortedDict[x][0])) # If not, return the selected variable
        
        return "3varTABU" # if all the varibale of unsatisfied clause are present in tabu list, return 3varTABU

""" Function to search for the solution of given instance """
def tabuSeacrh(instance, max_tries, max_flips, wp, tl, noVar):
    
    for t in range(max_tries): # Looping for the number of restarts i.e. 10
        
        tabuList = [] # list containing the variables which are tabu
        
        sol = [] # list containg the solution of given instance
        
        """ Generating random solution for the instance """
        for var in range(1, noVar+1):
            
            sol.append(random.choice([var,-var]))
    
        for flip in range(max_flips): # Looping for the number of flips i.e. 1000
            
            result = checkSatisfiability(instance, sol) # Checking satisfiability of the given solution
                    
            if result[0] == True: # checking if the given solution is satisfying the instance
                
                return sol # if yes, return the solution
            
            randClauIndex = random.randint(0, result[1]-1) # Select a random index from the range of number of unsatisfied clauses present in result[1]
            
            randUnsatClau = result[2][randClauIndex] # Selecting random unsatisfied clause from the list of unsatisified clauses
            
            solCopy = sol.copy() # Making a copy of the given solution
            
            bestVarToFlip = bestVariableToFlip(randUnsatClau, solCopy, instance, wp, tabuList) # Getting the best variable (having minimum number of unsatisfied clauses) to flip
            
            if bestVarToFlip == "3varTABU": # check if, all the variables are in tabu list
            
                continue # if yes, continue and select other unsatisfied clause
            
            else:
                
                if (len(tabuList) < tl): # if not, check if the tabu list if filled or not
                    
                    tabuList.append(bestVarToFlip) # if not, append the best variable to flip in tabu list
                    
                elif (len(tabuList) == tl): # check if tabu list is full
                                            # if yes,
                    tabuList.pop(0) # remove the first element from tabu list
                    tabuList.append(bestVarToFlip) # append the best variable to flip in tabu list
                    
            sol[bestVarToFlip - 1] = sol[bestVarToFlip - 1] * -1 # flip the best variable in the solution
            
    return "No Solution Found" # If no solution found, return "No Solution Found"
            
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print ("Error - Incorrect input")
        sys.exit(0)
    
    max_tries = 10 # number of maximum restarts
    max_flips = 1000 # number of maximum iterations
    wp = 0.3 # probability with which either random or best variable is selected
    tl = 5 # size of tabu list
    
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
        
        sol = tabuSeacrh(instance, max_tries, max_flips, wp, tl, noVar) # calling the tabuSearch function to find solution for the given instance file
        
        times.append(time.time()-t_start) # appending the tiken taken for the program to search for the solution
        print("Solution : ",sol) # printing the solution for the instance
        
    times.sort() # sorting the times list
    plt.plot(times,iterations) # plotting a graph of run-time and iterations
    plt.xlabel("run-time [CPU sec]")
    plt.ylabel("P(solve)")
    plt.title("Tabu Search for instance uf20-021.cnf")
    plt.show()