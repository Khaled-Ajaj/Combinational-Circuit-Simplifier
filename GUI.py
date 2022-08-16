########################################################
#  GUI Script for Constructing Digital Circuits
#  Written By: Khaled Ajaj - 7/20/2022
#  Description: This script creates a GUI for easily interacting with and passing
#  arguments to circuit.py
########################################################


import PySimpleGUI as sg
import subprocess
import sys

# runCommand(cmd)
# runs a command on the command line
# Arguments: a string of the command to run
# returns: the process number for the command that was run
def runCommand(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return p

# closeProcess(processNum)
# closes a running process
# Arguments: the process number as an integer
# returns: None
def closeProcess(processNum):
    if processNum:
        subprocess.Popen.terminate(processNum)


# generateNums(lo, hi)
# generates a string of numbers from lo to hi (inclusive), seperated by commas
# Arguments: the low bound and the high bound of the numbers, as integers.
# returns: a string of numbers seperated by commas
def generateNums(lo, hi):
    
    res = ""
    for i in range(lo, hi+1):
        res += str(i)
        res += ","
    
    return res

# formatRange(str)
# formats range input into input that is readable by the circuit.py program.
# Arguments: a string of input values
# returns: a string of numbers seperated by commas
def formatRange(str):
    newInput = ""
    tmp = ""
    indices = []
    
    # if the input has any ranges in it
    if "-" in str:
        str = str.split(",")
        
        # replace ranges with numbers
        for i, val in enumerate(str):
            if "-" in val:
                indices.append(val)
                n1, n2 = val.split("-")
                tmp += generateNums(int(n1), int(n2))
        
        # remove ranges from string
        for x in indices:
            str.remove(x)
        
        # join all numbers
        newInput = ",".join(str) + "," + tmp
        if newInput[-1] == ",": newInput = newInput[:-1]   

    # return formatted input
    return newInput if newInput else str


def main():
    cmd = ""
    processNum = None

    # window layout
    layout = [
        # [sg.Text("Combinational Circuit Simplifier", justification='left')],
        [sg.Text('Please enter minterms and don\'t cares (if any)')],
        [sg.Text("Minterms: ", justification='left'), sg.InputText("",size=(40,4),key="-MINTERMS-")],
        [sg.Text('                      Values: 0-1023')],
        [sg.Text("Don't Cares: ", justification='left'), sg.InputText("",size=(40,4),key="-DCS-")],
        [sg.Text('                      Values: 0-1023')],
        [sg.Button('Run'), sg.Button('Exit')],
        [sg.Text("Input must be comma seperated", justification='left')],
        [sg.Text("Example: 1,2,3,4,5", justification='left')]
    ]

    # create window
    window = sg.Window(title = "Combinational Circuit Simplifier Tool", layout = layout, margins = (100, 100))

    # Event Loop
    while True:             
            event, values = window.Read()

            # checks if user wants to exit
            if event in (None, 'Exit'):         
                closeProcess(processNum)
                break
            
            # if run button is clicked
            if event == 'Run':
                # close previous process of the same program if it is running
                if processNum:
                    closeProcess(processNum)
                
                # get inputs from text boxes
                input1 = values["-MINTERMS-"]
                input2 = values["-DCS-"]
                
                # format input
                input1 = formatRange(input1)          
                input2 = formatRange(input2)
                
                # pass input to program
                cmd = "python3 circuit.py " + "'" + "m(" + input1 + ")+d(" + input2 + ")" + "'"
                processNum = runCommand(cmd)


    # close window when done
    window.close()

if __name__ == "__main__":
    main()
