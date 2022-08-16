########################################################
#  Quine-McCluskey Method Class Implementation
#  Written By: Khaled Ajaj - 6/22/2022
#  Description: This class is a full implementation of the Quine McCluskey Algorithm for simplifying
#  combinational circuits using their minterms and "don't cares"
########################################################


import numpy as np
import math

class QMClass:

    # constructor
    def __init__(self):
        self.varLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


    # getNumVars(self, list)
    # determines the number of variables (bits) needed to represent the minterms
    # Arguments: list of minterms as integers
    # returns: an integer representing the required number of variables
    def getNumVars(self,list):

        # get max minterm
        maxNum = max(list)

        # edge case, only need one bit for a minterm of 0
        if max(list) == 0:
            return 1
        
        # find required num of vars
        else:
            return math.ceil(math.log2(maxNum+1))

    
    # createLiterals(self, binString)
    # generates literals to represent a binary string
    # Arguments: a binary string
    # returns: the literals representing the binary string, left to right
    def createLiterals(self,binString):
        literal = ""

        for i, bit in enumerate(binString):
            # add literal complement if 0
            if(bit == '0'):
                literal += self.varLetters[i]
                literal += "\'"
            
            # add literal if 1
            elif (bit == '1'):
                literal += self.varLetters[i]
            
        return literal  

    # compareTerms(self, term1, term2) 
    # check if the difference between two numbers is one bit only
    # Arguments: two terms, as binary strings, to compare between. The two terms must have the same length.
    # Returns: the index of the different bit if there is a single bit difference, otherwise -1.    
    def compareTerms(self, term1, term2):
        counter = 0
        index = -1

        # count number of different bits between two binary strings
        for i in range(len(term1)):
            if term1[i] != term2[i]:          
                counter += 1
                index = i
        
        if counter == 1:
            return index
        
        else:
            return -1
        


    # combineTerms(self, term1, term2) 
    # combine two terms that only have 1 bit difference
    # Arguments: two terms, as binary strings, with the same length.
    # Returns: the combined result of the two terms if they differ by excatly 1 bit, and 0 otherwise.
    def combineTerms(self, term1, term2):

        index = self.compareTerms(term1, term2)
        # if terms don't differ by exactly 1 bit
        if index == -1:
            return 0
        
        # if terms do differ by 1 bit only
        else:
            #replace the bit difference by - and return the new, combined term
            term1 = list(term1)
            term1[index] = '-'
            term1 = "".join(term1)
            return term1


    # combineGroups(self, group1, group2) 
    # combine two groups of minterms, where each group has the same number of 1s in their binary strings.
    # Arguments: two groups of terms, as binary strings.
    # Returns: two lists (combined, checklist), which represent
    # the combined result of the two groups and a checklist of the terms that were combined successfully.
    def combineGroups(self, group1, group2):
        combined = []
        checklist = []


        for x in group1:
            for y in group2:
                # combine terms between two groups of terms
                newCube = self.combineTerms(x, y)

                # if terms cannot be combined
                if not newCube:
                    continue

                # add new term to result and combined terms to checklist
                else: 
                    combined.append(newCube)
                    checklist.append(x)
                    checklist.append(y)
        
        return combined, checklist
        
        
        
    # checkCoverage(self, minterm, implicant) 
    # checks if a minterm is covered by an implicant
    # Arguments: two binary strings, a minterm, and an implicant
    # Returns: True if the minterm is covered by an implicant, false otherwise
    def checkCoverage(self, minterm, implicant):

        for i in range(len(minterm)):
            # check if the two bits are the same or the implicant has a don't care in that spot
            # if not, then minterm is not covered
            if (minterm[i] != implicant[i]) & (implicant[i] != '-'):
                return False
            else: 
                continue

        return True
            

    # createTable(self, PIList, mintermsList) 
    # create a Prime Implicant table
    # Arguments: two binary string lists: a prime implicant list, and a minterm list.
    # Returns: a table with boolean cells which containt True if minterm is covered by PI, and False otherwise.
    def createTable(self, PIList, mintermsList):
        table = [[] for x in range (len(PIList))]

        #check which minterms are covered by which prime implicants
        for i in range (len(mintermsList)):
            for j in range(len(PIList)):
                table[j].append(self.checkCoverage(mintermsList[i], PIList[j]))


        return table
        
        

    # groupLiterals(self, minterm) 
    # groups the literals of a minterm into a list
    # Arguments: a minterm, converted into literal form
    # Returns: a list containing the literals of the minterm
    def groupLiterals(self, minterm):
        literals = []
        str = ""
        for i in range(len(minterm)):
            str = ""
            # if its a letter
            if minterm[i] in self.varLetters:
                str = minterm[i]
                if ((i+1) < len(minterm)) and (minterm[i+1] == "'"):
                    str += "'"
            # if its a '
            if minterm[i] != "'":
                literals.append(str)
            
            
        
        return literals
        

    # sortTerm(self, minterm) 
    # sort the literals of the term in alphabetical order
    # Arguments: a string of minterm literals
    # Returns: the literal representation of the minterm as a string. 
    def sortTerm(self, minterm):
        
        # group the minterm literals
        sorted = self.groupLiterals(minterm)
        
        # sort in alphabetical order
        sorted.sort()

        # turn list into string
        sorted = "".join(sorted)

        return sorted
        

    # simplifications(self, mintermList) 
    # performs booelan algebra simpifications after taking the boolean AND of two boolean equations
    # Arguments: a list of literal strings
    # Returns: a list containing a simplified version of the input list
    def simplifications(self, mintermList):
        
        allCombos = []
        temp = []
        
        
        for i in range(len(mintermList)):
            temp = self.groupLiterals(mintermList[i])
            
            for j in range(len(mintermList)):
                
                count = 0
                if (mintermList[i] == mintermList[j]) and (i == j):
                    continue
                    # allCombos.append(mintermList[i])
                else:
                    for lit in temp:
                        if (lit in mintermList[j]):
                            count += 1

                    if count == len(temp):
                        
                        allCombos.append(mintermList[i])
        
        allCombos = list(set(allCombos))
        
        if allCombos:
            return allCombos
        else:
            return mintermList
        
    
    # andTerms(self, term1, term2) 
    # perform boolean AND between two terms
    # Arguments: two terms in their literal representation as strings
    # Returns: the boolean AND of the two terms, as a string. Empty string if the result is a boolean 0. 
    def andTerms(self, term1,term2): 
        

        # if either term is empty, return other term
        if not term1:
            return term2
        if not term2:
            return term1

        res = ""

        #group terms
        grouped1 = self.groupLiterals(term1)
        grouped2 = self.groupLiterals(term2)
        
        # perform boolean logic
        for var in grouped1:
            # AA' = 0
            if var+"'" in grouped2:
                return ""
            # AA = A
            else:
                res += var
            
        for var in grouped2:
            # A'A = 0
            if var+"'" in grouped1:
                return ""
            # AB = AB
            elif var not in grouped1:
                res += var
        
        # sort resulting term alphabetically
        res = self.sortTerm(res)
        return res

    
    
    # andEquations(self, eq1, eq2) 
    # boolean AND two boolean equations
    # Arguments: two lists of literal strings
    # Returns: the boolean AND of the two lists, as a new list of literal strings
    def andEquations(self, eq1, eq2):
        
        # if either equation is empty, return the other
        if not eq1:
            return eq2
        if not eq2:
            return eq1
        
        res = []

        # AND each term in the two equations together
        for i in eq1:
            for j in eq2:
                tmp = self.andTerms(i,j)
                res.append(tmp) if tmp else None
        
        return res


    # petricksMethod(self, minTermCover) 
    # performs Petrick's Method on the minterm covers 
    # Arguments: a list of literal strings (terms)
    # Returns: the result of petrick's method on the input, as a list of literal strings.
    def petricksMethod(self, minTermCover):
        result = []
        
        for eq in minTermCover:
            # keep track of the previous result
            prevRes = result.copy()
            # take the boolean AND of the previous result and the current equation
            result = self.andEquations(result, eq)

            # while the result is not fully simplified, keep simplifying 
            while (not np.array_equal(result, prevRes)):
                prevRes = result.copy()
                result = self.simplifications(result)

        #remove redundancies
        result = list(set(result))
        return result
        

    # cost(self, PI, numVariables) 
    # calculates the hardware cost of a prime implicant
    # Arguments: a prime implicant, as a string of literals, and the number of term variables as an integer.
    # Returns: the hardwarre cost of the prime implicant, as an integer
    def cost(self, PI, numVariables):
        cube = self.groupLiterals(PI)
        cubeSize = numVariables-len(cube)
        
        return (numVariables-cubeSize)

    

    # minCost(self, eq1, eq2) 
    # finds the prime implicants with the minimum hardware cost
    # Arguments: a list of PIs in their literal representation
    # Returns: a list of the PIs with the lowest hardware cost
    def minCost(self, PI):
        costs = []
        index = []
        minCosts = []

        # find costs for each term
        for term in PI:
            costs.append(self.cost(term, len(term)))
        
        # find terms with the same cost
        for i in range(len(costs)):
            if costs[i] == min(costs):
                index.append(i)
        
        # append terms with min cost to result
        for i in index:
            minCosts.append(PI[i])
        
        return minCosts
        
    
    # complement(self, equation) 
    # Complements a Sum of Products boolean equation into a Product of Sums boolean equation
    # Arguments: a Sum of Products boolean equation as a string
    # Returns: a Product of Sums boolean equation as a string
    def complement(self, equation):
        # split terms
        eq = equation.split(" + ")

        result = "("

        for term in eq:

            # str = ""
            # for i in range(len(term)):
            #     # complement every literal in the term
            #     if term[i] in self.varLetters:
            #         str += term[i]
                    
            #         if (i+1 == len(term)):
            #             str += "'"
                    
            #         elif (term[i+1] == "'"):
            #             continue
                    
            #         else: 
            #             str += "'"
            
            grouped = self.groupLiterals(term)
            for i, lit in enumerate(grouped):
                if len(lit) == 1:
                    grouped[i] = lit + "'"
                else:
                    grouped[i] = lit[0]
            
            result += " + ".join(grouped)
            result += ")("
            # for i in range(len(grouped)):
            #     result += grouped[i]
            #     if (i+1 != len(grouped)):
            #         result += " + "
            #     else:
            #         result +=")("
                    
        result = result[:-1]
        return result        
        
        
    # printSolution(self, solution) 
    # generates a string containing the POS form of a solution
    # Arguments: a list containing the terms of the solution
    # Returns: a string containing the elements of the list joined by + characters.
    def printSolution(self, solution):
        return " + ".join(solution)
    

    # printAllSolutions(self, solution, closeCover, solType) 
    # generates the output of the program
    # Arguments: two lists containing the terms of the solution and the close cover, and a string indicating
    # the type of boolean equation ("SOP" or "POS")
    # Returns: None
    def printAllSolutions(self, solution, closeCover, solType):
        
        print("=====================")
        print("Solution is: ")
        
        str = ""

        # if there are close cover terms
        if closeCover:
            for i in range(len(closeCover)):
                # add one of the close cover terms to the solution and print solution option
                if solution:
                    str = self.printSolution(solution)
                    str += " + "
                str += closeCover[i]

                # print based on solution type
                if solType == "SOP":
                    print(str)
                elif solType == "POS":
                    print(self.complement(str))
                
                if (i < len(closeCover)-1):
                    print("\n\tOR\n")

        # if there is no solution or close cover
        elif not solution:
            print("There is no solution for the provided function.")
        
        # if there is only solution terms
        else: 
            str = self.printSolution(solution)
            if solType == "SOP":
                print(str)
            elif solType == "POS":
                print(self.complement(str))

        print("=====================")  
        
        


    # findEPI(self, table, PIList, mintermList) 
    # determines the essential prime implicants of a set of minterms
    # Arguments: the PI table, a list of prime implicants, and a list of minterms
    # Returns: a list of the essential prime implicants
    def findEPI(self, table, PIList, mintermList):

        essentialPrimes = []
        for i in range(len(mintermList)):
            # count the number of PIs the minterm is covered by
            count = 0
            for j in range(len(PIList)):
                if table[j][i] == True:
                    count += 1
                    temp = PIList[j]
            
            # if a minterm is only covered by one PI, then it's an EPI
            if count == 1:
                essentialPrimes.append(temp)

        # remove duplicates
        essentialPrimes = list(set(essentialPrimes))
        return essentialPrimes
        
        
    # readFile(self, filname) 
    # reads inputs from a file
    # Arguments: a string indicating the filename to read from
    # Returns: a list of the lines in the file as strings
    def readFile(self, filename):
        file1 = open(filename, 'r')
        lines = file1.readlines()
        
        for i in range(len(lines)):
            lines[i] = lines[i].strip("\n")

        return lines
        

    # printSolution(self, cubes, allBin, numVariables) 
    # generates cube groups for the first step of the algorithm
    # Arguments: a 3-d array for cubes, a list containing minterms and don't cares in binary form, and the number of
    # bits the algorithm is using as an integer.
    # Returns: None
    def generateCubes(self,cubes, allBin, numVariables):
        # cubes[i][j][k] : i is cube num, j is group num, k is minterm
        for i in allBin:
            for j in range(numVariables+1):
                if i.count('1') == j:
                    cubes[0][j].append(i)
                    break
    
    # checkCubes(self, cubes, numVariables) 
    # checks cubes that are combined into higher cubes
    # Arguments: a 3-d array of cubes, and the number of bits the algorithm is using as an integer.
    # Returns: a list of checked cubes.
    def checkCubes(self, cubes, numVariables):
        checkedCubes = []

        # combine groups and check combined groups
        for i in range(0, numVariables):
            for j in range(0, numVariables):
                cubes[i+1][j], check = self.combineGroups(cubes[i][j], cubes[i][j+1])
                checkedCubes += check
                
                
        # remove redundant cubes        
        for i in range (numVariables+1):
            for j in range (numVariables+1):
                cubes[i][j] = list(set(cubes[i][j]))

        checkedCubes = list(set(checkedCubes))
        return checkedCubes

    # findPI(self, cubes, checkedCubes, numVariables) 
    # finds prime implicants from combined cubes
    # Arguments: a 3-d array for cubes, a list of checked cubes, and the number of bits as an integer.
    # Returns: a list of the prime implicants
    def findPI(self, cubes, checkedCubes ,numVariables):
        # finding prime implicants
        primeImps = []
        for i in range (numVariables+1):
            for j in range (numVariables+1):
                for term in cubes[i][j]:
                    # all the non-checked terms in the table are prime implicants
                    if term not in checkedCubes:
                        primeImps.append(term)
        
        return primeImps


    # reduceTable(self, essentialPrimes, mintermsBin, reducedMinterms, primeImps, solution) 
    # removes essential primes and the minterms they cover from PI table
    # Arguments: lists of essential primes, mintems in binary form, the list to store the reduced minterms in, a list
    # of prime implicants, and the lost to sore solution in.
    # Returns: None
    def reduceTable(self, essentialPrimes, mintermsBin, reducedMinterms, primeImps, solution):
        for ep in essentialPrimes:
        
            for term in mintermsBin:
                if self.checkCoverage(term, ep):
                    if term in reducedMinterms:
                        reducedMinterms.remove(term)
            if ep in primeImps:
                primeImps.remove(ep)


        for ep in essentialPrimes:
            solution.append(self.createLiterals(ep))


    # rowDominance(self, primeImps, reducedMinterms, table, PIList) 
    # performs row dominance on reduced PI table
    # Arguments: lists of PIs, reduced minterms, PI table, and a copy of the PI list 
    # Returns: None
    def rowDominance(self, primeImps, reducedMinterms, table, PIList):
        toRemove = []
        
        for i in range(len(primeImps)):
            # count how many minterms are covered by PI
            count = 0 
            for j in range(len(reducedMinterms)):
                if table[i][j]:
                    count += 1 
    
            # if PI covers only one minterm, remove it
            if count == 1:
                toRemove.append(primeImps[i])
            
        # remove all PIs that only cover one term
        for x in toRemove:
            if x in primeImps:
                PIList.remove(x)


    # colDominance(self, primeImps, reducedMinterms, table, PIList) 
    # performs column dominance on reduced PI table
    # Arguments: PI table, reduced minterms, prime implicants, copy of reduced minterms. 
    # Returns: None
    def colDominance(self, table, reducedMinterms, primeImps, minterms):
            #column dominance
            toRemove = []
            for i in range(len(reducedMinterms)):
                # count number of prime implicants that cover each minterm 
                count = 0 
                for j in range(len(primeImps)):
                    if table[j][i]:
                        count += 1
                
                # if a minterm is covered by all PIs then remove it
                if count == len(primeImps):
                    toRemove.append(reducedMinterms[i])
            
            for x in toRemove:
                if x in reducedMinterms:
                    minterms.remove(x)  


    # findCloseCover(self, reducedMinterms, primeImps, table) 
    # finds the close cover of the solution
    # Arguments: a list of reduced minterms, a list of prime implicants, and the PI table 
    # Returns: a list of close cover terms
    def findCloseCover(self, reducedMinterms, primeImps, table):

        minTermCover = [[] for x in reducedMinterms]
        # turn prime implicants of each minterm into boolean literals
        for i in range(len(reducedMinterms)):
            for j in range(len(primeImps)):
                if table[j][i]:
                    minTermCover[i].append(self.createLiterals(primeImps[j]))

        # perform petrick's method   
        closeCover = self.petricksMethod(minTermCover)

        # find close covers with the minimum cost
        closeCover = self.minCost(closeCover)

        return closeCover

    # reduceRemaining(self, primeImps, reducedMinterms, table, PIList) 
    # This function runs the algorithm for creating reduced PI table and for finding the close cover 
    # if there are minterms not covered by EPIs.  
    # Arguments: lists of PIs, reduced minterms, all minterms in binary form, EPIs, solution, and list to store close cover in.
    # Returns: None
    def reduceRemaining(self, primeImps, reducedMinterms, mintermsBin, essentialPrimes, solution, closeCover):
        # create reduced PI table
        table = self.createTable(primeImps, reducedMinterms)
        piCpy = primeImps.copy()
        minCpy = reducedMinterms.copy()


        #row dominance 
        self.rowDominance(primeImps, reducedMinterms, table, piCpy)
        
        # column dominance
        self.colDominance(table, reducedMinterms, primeImps, minCpy)
        
        # update reduced PI table and find new essential prime
        if piCpy and minCpy: 
            primeImps = piCpy
            reducedMinterms = minCpy       
            table = self.createTable(piCpy, minCpy)
            essentialPrimes = self.findEPI(table, piCpy, minCpy)
            
  
        self.reduceTable(essentialPrimes, mintermsBin, reducedMinterms, primeImps, solution)
        
        # remove duplicates
        solution = list(set(solution))

        # if there are still minterms not covered after reducing reduced table, find close cover
        if reducedMinterms:
            closeCover = self.findCloseCover(reducedMinterms, primeImps, table)
        
        return solution, closeCover

    # qmMethod(self, mintermsList, dontCaresList, allList, numVariables) 
    # performs QM Method
    # Arguments: integer lists of minterms, dont cares, all inputs, and the number of bits to perform QM on
    # Returns: None
    def qmMethod(self, mintermsList, dontCaresList, allList, numVariables):
        solution = []
        closeCover = []
        
        # creating binary representation of terms
        numBits = "0"+ str(numVariables) +"b"
        allBin = [(format(x, numBits)) for x in allList]

        mintermsBin = [(format(x, numBits)) for x in mintermsList]
        # dont_cares_bin = [(format(x, numBits)) for x in dontCaresList]

        # creating cubes matrix
        cubes = [[[] for row in range(numVariables+1)] for x in range(numVariables+1)]

        

        

        essentialPrimes = []

        # group into cubes
        self.generateCubes(cubes, allBin, numVariables)
        
        # combine and check cubes
        checkedCubes = self.checkCubes(cubes, numVariables)

        # find prime implicants
        primeImps = self.findPI(cubes, checkedCubes, numVariables)
                    

        # making PI chart and finding essential primes

        table = self.createTable(primeImps, mintermsBin)



        # finding essential primes

        essentialPrimes = self.findEPI(table, primeImps, mintermsBin)



        # exclude essential primes from reduced implicant table

        reducedMinterms = mintermsBin.copy()

        
        self.reduceTable(essentialPrimes, mintermsBin, reducedMinterms, primeImps, solution)
        

        # if there are still minterms not covered, find close cover
        if reducedMinterms:
            solution, closeCover = self.reduceRemaining(primeImps, reducedMinterms, mintermsBin, essentialPrimes, solution, closeCover)
        
                
        return solution, closeCover

    # formatInput(self, input) 
    # splits input into lists of minterms and don't cares
    # Arguments: a string of the input
    # Returns: two lists: minterms, and don't cares.
    def formatInput(self, input):
        # terms = [minterms, don't cares]
        terms = input.split("+")
        minterms = ""
        dontCares = ""
        minterms = terms[0].strip("m()")
        
        # if there are don't care values
        if (len(terms) > 1):
            dontCares = terms[1].strip("d()")
        return minterms, dontCares

    # runQM(self, input) 
    # runs QM method
    # Arguments: string input into program
    # Returns: two lists: solution, close cover
    def runQM(self, input):

        #  format program input into function inputs
        minterms, dontCares = self.formatInput(input)
        minterms = [int(x) for x in minterms.split(",")]
        
        if dontCares:
            dontCares = [int(x) for x in dontCares.split(",")]
            all = minterms + dontCares
        else:
            all = minterms

        all.sort()
        
        # get num of bits for algorithm
        numVariables = self.getNumVars(all)
        
        # maxterms for POS form
        maxterms = []

        # find maxterms from minterms
        for i in range(2**(numVariables)):
            if (i not in minterms):
                maxterms.append(i)

        # print program output
        print("Solution for: " + input)
        print("=========================")
        print("=========================")
        print("SOP form:")            
        solution, closeCover = self.qmMethod(minterms, dontCares, all, numVariables)
        self.printAllSolutions(solution, closeCover, "SOP")
        print("POS form:")   
        solution, closeCover = self.qmMethod(maxterms, dontCares, maxterms, numVariables)
        self.printAllSolutions(solution, closeCover, "POS")
        print("=========================")

        solution, closeCover = self.qmMethod(minterms, dontCares, all, numVariables)
        # if solution:
        #     solution = solution.sort()
        # if closeCover:
        #     closeCover = closeCover.sort()
        return solution, closeCover


def main():

        mode = input("Read from file? [yes/no]: ")
        qm = QMClass()

        # if reading from file, run QM for each line
        if (mode == "yes"):
            filename = input("what is the filename? ")
            inputs = qm.readFile(filename)
            
            for eq in inputs:
                qm.runQM(eq)
                print("\n\n\n")
        
        # read from terminal input
        else:
            
            eq = input("Please enter the minterms and don't cares: ")
            qm.runQM(eq)


if __name__ == "__main__":
    main()

