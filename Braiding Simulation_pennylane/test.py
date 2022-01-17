import pennylane as qml
import numpy as np
dev = qml.device("default.qubit", wires = 1)
H = qml.Hamiltonian(
    [1],
    [qml.PauliZ(0)])

t = 1
@qml.qnode(dev)
def circuit():
    qml.templates.ApproxTimeEvolution(H, t, 100)
    return qml.state()

print(circuit())
print(np.exp(-1j))