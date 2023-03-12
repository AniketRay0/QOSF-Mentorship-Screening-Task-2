from pyquil import Program, get_qc
from pyquil.gates import *
from pyquil.quilbase import Declare
def is_rectangle(A, B, C, D):
    inputs = [A, B, C, D]
    maxBits = max(len(bin(x)[2:]) for x in inputs)
    inputsBin = [[int(x) for x in bin(i)[2:].zfill(maxBits)[::-1]] for i in inputs]
    inputCombos = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
    bitstringsList = []
    for combo in inputCombos:
        p = Program()  # Reset the program to an empty program
        ro = p.declare('ro', 'BIT', 1)
        for i in range(4):
            for j in range(maxBits):
                if inputsBin[i][j]==1:
                    p += X(i*maxBits+j)
        for k in range(maxBits):
            p += CNOT(combo[0]*maxBits+k, 4*maxBits+k)
            p += CNOT(combo[1]*maxBits+k, 4*maxBits+k)
            p += X(4*maxBits+k)
        p += X(5*maxBits).controlled(range(4*maxBits, 5*maxBits))
        p += MEASURE(5*maxBits, ro[0])
        qc = get_qc('29q-qvm')  
        executable = qc.compile(p)
        result = qc.run(executable) 
        bitstrings = result.readout_data.get('ro')
        bitstringsList.append(bitstrings[0][0])
    
    p = Program()
    ro = p.declare('ro', 'BIT', 1)
    for i in range(6):
        if bitstringsList[i]==1:
            p += X(i)
    p+=CCNOT(0,5,6)
    p+=X(6)
    p+=CCNOT(1,4,7)
    p+=X(7)
    p+=CCNOT(2,3,8)
    p+=X(8)
    p+=X(9).controlled([6,7,8])
    p+=X(9)
    p += MEASURE(9, ro[0])
    qc = get_qc('10q-qvm')  
    executable = qc.compile(p)
    result = qc.run(executable) 
    bitstrings = result.readout_data.get('ro')
    return bitstrings[0][0]