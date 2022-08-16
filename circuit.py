########################################################
#  Circuit Constructor Script
#  Written By: Khaled Ajaj - 7/15/2022
#  Description: This Script utilizes the QM class to create a schematic of a simplified
#  combinational circuit based on passed minterms and "don't care" values utilizing the 
#  schemdraw library
########################################################



from cProfile import label
import schemdraw
from schemdraw.parsing import logicparse
import schemdraw.elements as elm
import QM
import sys

# generateEquations(solutions, closeCover) 
# generates boolean equations to draw as schematics
# Arguments: a list containing QM solution terms, and a list containing QM close cover terms
# Returns: None
def generateEquations(solutions, closeCover):
    
    if closeCover:
        return [solutions + [i] for i in closeCover]
    
    return [solutions]


# formatLiterals(literals) 
# formats literals to display properly as labels on schematic
# Arguments: a list of literals
# Returns: None   
def formatLiterals(literals):
    for i, lit in enumerate(literals):
            if len(lit) == 2:
                literals[i] = "$\\overline{" + lit[0]  + "}" + "$"


# generateLiterals(term) 
# splits formatted literals into their own index in a list 
# Arguments: a string of a solution term
# Returns: a list of literals from the term
def generateLiterals(term):
    lits = []

    # group literals
    for i, literal in enumerate(term):
        if literal == "'":
            lits[-1] += "'"
            continue
        lits.append(literal)
    
    formatLiterals(lits)
    return lits


# buildwires(term, wires, totalAndGates, drawing) 
# adds wires (terms with only one literal) to schematic
# Arguments: the term (string), wires (list), totalAndGates (2-d list), drawing (schemdraw drawing type) 
# Returns: None  
def buildWires(term, wires, totalAndGates,drawing):

    # add wires to list and label them
    if len(term) == 1:
        wires.append(schemdraw.logic.Dot().label(term[0] + "    "))
    
    # draw wires on schematic
    for i, wire in enumerate(wires):
        # draw under first wire if it exists
        if i > 0:
            x, y = wires[i-1].center
            drawing += wire.at((x, y-1))

        # if there are and gates above it, draw under and gates
        elif totalAndGates:
            drawing+= wire.at(totalAndGates[-1][0].in2, dy = -1.5*(len(totalAndGates[-1])))
        
        # if theres nothing in schematic yet, draw in default spot
        else:
            drawing+= wire



# drawGates(gate1, gate2, newGate, drawing, mode) 
# draws a new gate that connects two previous gates/wires
# Arguments: the two gates to connect, the new gate, the drawing to draw to, the mode
# mode 0 is two gates, mode 1 is two wires, mode 2 is gate and wire (for mode 2, gate1 must be the wire)
# Returns: None 
def drawGates(gate1, gate2, newGate, drawing, mode):
        x1, y1, x2, y2 = 0, 0, 0, 0

        # mode == 0 , two gates
        if not mode:
            x2,y2 = gate1.out
            x1,y1 = gate2.out
        
        # mode == 1, two wires
        elif mode == 1:
            x1,y1 = gate1.center
            x2,y2 = gate2.center
        
        # mode == 2, wire and gate
        else:
            x2,y2 = gate1.center
            x1,y1 = gate2.out

        # difference in height between two gates
        diff = y2-y1

        #connect two gates (in original gate) by drawing wires.
        drawing += newGate.at((max(x1,x2),y2) , dx = 1.5, dy = -diff/2).theta(0)
        drawing+= schemdraw.logic.Line().at((x1,y1)).tox(newGate.in1)
        drawing+= schemdraw.logic.Line().at(newGate.in1).toy((x1,y1))
        drawing+= schemdraw.logic.Line().at((x2,y2)).toy(newGate.in2)
        drawing+= schemdraw.logic.Line().at(newGate.in2).tox((x2,y2))
        


# connectAndGates(andGates, orGates, drawing) 
# connects and gate groups together with or gates
# Arguments: 2-d array of and gates, a list of or gates, and the schematic to draw to
# Returns: None
def connectAndGates(andGates, orGates, drawing):

    # use this as a stack
    cpy = andGates.copy()

    # while stack has more than 1 group of andgates, pop last 2 groups and connect them with or gate
    while len(cpy) > 1:
        
        #create new or gate
        newGate = schemdraw.logic.Or()

        #pop last two or gates off the queue
        
        gate1 = cpy.pop(0)[-1]
        gate2 = cpy.pop(0)[-1]

        drawGates(gate1, gate2, newGate, drawing, 0)

        #add new gate to queue
        orGates.append(newGate)

    # edge case: if there is an odd number of and gate groups, connect last group with latest added or gate
    if len(cpy) == 1 and orGates:
        #create new or gate
        newGate = schemdraw.logic.Or()

        #pop last two or gates off the queue
        
        gate1 = cpy.pop(0)[-1]
        gate2 = orGates.pop(0)

        drawGates(gate1, gate2, newGate ,drawing, 0)


        #add new gate to queue
        orGates.append(newGate)



# connectWires(wires, orGates, drawing) 
# connects wires (terms with no and gates), together using or gates
# Arguments: a list of wires, a list of or gates, and the schematic to draw to.
# Returns: None
def connectWires(wires, orGates, drawing):

    # stack of wires
    cpy = wires.copy()

    # connect all wires together
    while len(cpy) > 1:
        
        #create new or gate
        newGate = schemdraw.logic.Or()

        #pop last two or gates off the queue
        
        gate1 = cpy.pop(0)
        gate2 = cpy.pop(0)

        drawGates(gate1, gate2, newGate, drawing, 1)

        #add new gate to queue
        orGates.append(newGate)

    # edge case: if there is an odd number of wires, connect last or gate with last wire
    if len(cpy) == 1 and orGates:
        #create new or gate
        newGate = schemdraw.logic.Or()

        #pop last two or gates off the queue
        
        gate1 = cpy.pop(0)
        gate2 = orGates.pop(0)

        drawGates(gate1, gate2, newGate , drawing, 2)


        #add new gate to queue
        orGates.append(newGate)



# buildOrGates(drawing, orGates, totalAndGates, wires) 
# builds or gates for and gates and wires
# Arguments: schematic to draw to, list of or gates, 2-d list of and gates, list of wires
# Returns: None
def buildOrGates(drawing, orGates, totalAndGates, wires):
    connectAndGates(totalAndGates, orGates, drawing)
    connectWires(wires, orGates, drawing)
        

# buildAndGates(term, totalAndGates, drawing) 
# builds and gates for a term and connects them together
# Arguments: a string indicating the term to draw, a 2-d array of the total and gates in the schematic,
# the drawing to draw gates to.
# Returns: None
def buildAndGates(term, totalAndGates, drawing):
    
    # if term only has 1 literal, doesn't need and gates.
    if len(term) == 1:
        return

    # this term's and gates
    andGates = []

    # create and gates for every literal
    for i, literal in enumerate(term):

        # second literal is an edge case.
        # doesn't need it's own and gate
        if (i==0):
            andGates.append(schemdraw.logic.And().label(literal, 'in1'))
            continue
        if (i == 1):
            andGates[0].label(literal, 'in2')
            continue

        andGates.append(schemdraw.logic.And().label(literal, 'in2'))

        

    # add gates to drawing
    for i, gate in enumerate(andGates):
        # if the gate is not the first gate in its term, draw it below the previous and gate
        if i > 0:
            drawing+= gate.at(andGates[i-1].out, dy = -1)

        # if the gate is the first one in its term, draw it under the last gate from the previous term
        # line it up with the first gate from the last term in the x-direction
        elif totalAndGates:
            drawing+= gate.at(totalAndGates[-1][0].out, dx = -2, dy = -1 - len(totalAndGates[-1])).theta(0)
        
        # if it's the first gate added to the drawing, draw it in the default location
        else:
            drawing += gate.theta(0)
    
    # connect the gates with wires
    for i, gate in enumerate(andGates):
        if i > 0:
            drawing+= schemdraw.logic.Line().at(andGates[i-1].out).to(gate.in1)
    
    # add all the term's gates to the total gates list
    totalAndGates.append(andGates)
    
            
# addLabels(drawing, orGates, totalAndGates, wires, sol, close) 
# adds final labels to circuit and prints the boolean equation
# Arguments: the drawing to draw to, the list of or gates, the 2-d list of total and gates, the list
# of wires, the list of solutions, and the list of close covers.
# Returns: None
def addLabels(drawing, orGates, totalAndGates, wires, sol, close):

    # mark output gate if or gate
    if orGates:
        drawing+=orGates[0].label("Output", 'out')
    
    # mark output gate if and gate
    elif totalAndGates:
        drawing+=totalAndGates[-1][-1].label("Output", 'out').theta(0)
    

    # printing the simplified boolean equation
    title = "F = "
    title += " + ".join(sol)

    # adding close cover term if applicable
    if close:
        if sol:
            title += " + "
    
        title += close[0]

    # lining up the boolean equation with the drawing
    boxList = [ item for innerlist in totalAndGates for item in innerlist ] + wires
    drawing += (phase1 := elm.EncircleBox(boxList , padx=5, pady=.5).linestyle('').linewidth(2).color('black')
            .label(title, loc='top', rotate=0))


# connectRemaining(orGates, wires, totalAndGates, drawing) 
# connects unconnected or gates between and gate terms and wire terms.
# Arguments: list of or gates, list of wires, 2-d list of total and gates, and the drawing to draw to.
# Returns: None
def connectRemaining(orGates, wires, totalAndGates, drawing):

    # number of terms with wires/and gates only
    andCount, wireCount = len(totalAndGates), len(wires)

    # crate new or gate to connect last two or gates
    newGate = schemdraw.logic.Or()

    gate1, gate2 = None, None
    mode = 0

    # if there are no previous or gates, connect to wire and gate directly
    if andCount == 1 and wireCount == 1:
        gate1 = wires[-1]
        gate2 = totalAndGates[-1][-1]
        mode = 2


    # if there is an or gate connected to wires, connect and gate and or gate
    elif andCount == 1 and wireCount > 1:
        gate1 = orGates.pop(0)
        gate2 = totalAndGates[-1][-1]
    
    
    # if there are or gates connected to and gates and wires, connect last two or gates.
    elif andCount > 1 and wireCount > 1:
        gate1 = orGates.pop(0)
        gate2 = orGates.pop(0)

    # connect gates/wires  
    if gate1 and gate2:
        drawGates(gate1, gate2, newGate, drawing, mode)
        orGates.append(newGate)


    
    
    #connect remaining or gates
    while len(orGates) > 1:

        #create new or gate
        newGate = schemdraw.logic.Or()

        #pop last two or gates off the queue
        
        gate1 = orGates.pop(0)
        gate2 = orGates.pop(0)

        
        drawGates(gate1, gate2, newGate, drawing, 0)

        #add new gate to queue
        orGates.append(newGate)





def main():
    # commad line arguments
    args = sys.argv

    if len(args)==1:
        print("USAGE: circuit.py terms [fileName]")
        return

    # create instance of QM class
    algo = QM.QMClass()

    # run the algorithm
    sol, close = algo.runQM(args[1])

    # sort the solution list for alphabetical ordered solution
    sol.sort()

    # generate equations from the solution to feed into circuit drawing functions
    equations = generateEquations(sol, close)



    # lists of gates and wires in drawing for easy access 
    totalAndGates = []
    orGates = []
    wires = []

    # new drawing
    drawing = schemdraw.Drawing()

    # pick the first solution
    eq = equations[0]

    # for every term in the equation, generate and gates and wires
    for t in eq:
        lit = generateLiterals(t)
                
        buildAndGates(lit, totalAndGates, drawing)
        buildWires(lit, wires, totalAndGates ,drawing)
    
    # connect unconnected ends with or gates
    buildOrGates(drawing, orGates, totalAndGates, wires)
    connectRemaining(orGates, wires, totalAndGates, drawing)
    
    # add finals labels to drawing
    addLabels(drawing, orGates, totalAndGates, wires, sol, close)
    
    # create drawing
    drawing.draw()

    # option for saving drawing
    if len(args) == 3:
        drawing.save(f"{args[2]}.jpg", dpi = 1000)



if __name__ == "__main__":
    main()
 