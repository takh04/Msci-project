import pennylane as qml
from pennylane import numpy as np

def initialize(state, d_min, d_max):
    d1, d2, d3 = d_min, d_min, d_max
    d = (d1**2 + d2**2 + d3**2)**(1/2)
    if state == 'plus':
        statevector = np.array([1j * (d + d3), 0, 0, d1 + 1j * d2])
        statevector = statevector / np.linalg.norm(statevector)
        print("Initial State is: " + str(statevector))
    elif state == 'minus':
        statevector = np.array([0, 1j * (d - d3), d1 + 1j * d2, 0])
        statevector = statevector / np.linalg.norm(statevector)
        print("Initial State is: " + str(statevector))
    else:
        print("Non-valid initial state")
    qml.templates.AmplitudeEmbedding(statevector, wires=[0,1], normalize=True)