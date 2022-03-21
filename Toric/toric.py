import pennylane as qml
from pennylane import numpy as np
import toric_hamiltonian

boundary_condition, dimension = 'mixed', '3by3'
logical_state = 'arbitrary'
theta = np.pi / 2
logical_state_vector = theta
A, B = 1, 1
qubits, H = toric_hamiltonian.toric_code_hamiltonian(A, B, dimension, boundary_condition)
dev1 = qml.device("default.qubit", wires=qubits)

@qml.qnode(dev1)
def check(logical_state):
    toric_hamiltonian.toric_code_ground(dimension, boundary_condition, logical_state, logical_state_vector)
    return qml.expval(H)


print(check(logical_state))


