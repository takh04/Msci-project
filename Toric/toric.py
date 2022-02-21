import pennylane as qml
from pennylane import numpy as np
import toric_hamiltonian


A, B, M, N = 1, 1, 4, 4
H = toric_hamiltonian.toric_hamiltonian(A, B, M, N)
qubits = []
for n in range(N):
    for m in range(2*M):
        q = 'q' + str(n) +',' + str(m)
        qubits.append(q)
dev = qml.device("default.qubit", wires=qubits)


@qml.qnode(dev)
def check():
    toric_hamiltonian.toric_ground_state(M,N)
    return qml.expval(H)

print(check())





