# QOSF-Mentorship-Screening-Task-2

## Introduction: 
The file is_rectangle.py defines a function that takes in 4 integers and creates quantum circuits that eventually output "0" if they don't form a rectangle and "1" if they do.
The function has some limitations, which are mentioned later, but uses the pyquil library and is compatible with the Rigetti QVM.

## Design:
The program first converts the integers into binary digits and stores them in a list. Then it compares the sides A,B,C,D (6 comparisons total) by creating a loop that creates a quantum circuit and measures the result into a classical bit for each of the 6 comparisons. 
This is stored in a list of 6 elements which are either 1 (sides are equal) or 0 (sides are not equal). Then another quantum circuit checks if A=B and C=D or A=C and B=D or A=D and B=C, and if one of them is true then they form a rectangle and the circuit measures the output as 1 if they do and 0 if they don't.

## Limitations: 
Since the QVM supports a maximum of 29 qubits and the circuit depends on the size of the inputs, the inputs can use a maximum of 5 binary digits, so numbers below 63.
