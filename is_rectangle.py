from pyquil import Program, get_qc
from pyquil.gates import *
from pyquil.quilbase import Declare

def is_rectangle(A, B, C, D):
    #Converting inputs into binary
    inputs = [A, B, C, D]
    maxBits = max(len(bin(x)[2:]) for x in inputs)
    inputsBin = [[int(x) for x in bin(i)[2:].zfill(maxBits)[::-1]] for i in inputs]
    #Loop over combinations of sides to compare
    inputCombos = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
    bitstringsList = []
    for combo in inputCombos:
        #Creates a quantum circuit to compare two sides
        p = Program() 
        ro = p.declare('ro', 'BIT', 1)
        #initialize qubits to match binary digits
        for i in range(4):
            for j in range(maxBits):
                if inputsBin[i][j]==1:
                    p += X(i*maxBits+j)
        #Compare sides digit by digit
        for k in range(maxBits):
            p += CNOT(combo[0]*maxBits+k, 4*maxBits+k)
            p += CNOT(combo[1]*maxBits+k, 4*maxBits+k)
            p += X(4*maxBits+k)
        p += X(5*maxBits).controlled(range(4*maxBits, 5*maxBits))
        p += MEASURE(5*maxBits, ro[0])
        #run the circuit on qvm
        qc = get_qc('29q-qvm')  
        executable = qc.compile(p)
        result = qc.run(executable) 
        bitstrings = result.readout_data.get('ro')
        #store result in bitstringsList
        bitstringsList.append(bitstrings[0][0])
    
    #New circuit to compare results in bitstringsList
    p = Program()
    ro = p.declare('ro', 'BIT', 1)
    #initialize qubits
    for i in range(6):
        if bitstringsList[i]==1:
            p += X(i)
    #Checks (A=B and C=D) or (A=C and B=D) or (A=D and B=C)
    p+=CCNOT(0,5,6)
    p+=X(6)
    p+=CCNOT(1,4,7)
    p+=X(7)
    p+=CCNOT(2,3,8)
    p+=X(8)
    p+=X(9).controlled([6,7,8])
    p+=X(9)
    #run the circuit on qvm
    p += MEASURE(9, ro[0])
    qc = get_qc('10q-qvm')  
    executable = qc.compile(p)
    result = qc.run(executable) 
    bitstrings = result.readout_data.get('ro')
    #returns 0 if they don't form a rectangle and 1 if they do
    return bitstrings[0][0]
