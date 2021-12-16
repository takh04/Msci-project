import pennylane as qml
from pennylane import numpy as np

def initialize(state, a,d_min, d_max, system):
    if system == 'Beenakker':
        initialize_Beenakker(state, d_min, d_max)
    elif system == 'Stenger':
        initialize_Stenger(state, a, d_min, d_max)


def initialize_Beenakker(state, d_min, d_max):
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


def initialize_Stenger(state, a, d_min, d_max):
    d1, d2, d3 = d_max, d_min, d_min
    d = (d1**2 + d2**2 + d3**2)**(1/2)
    D = (d1**2 + d2**2 + d3**2 + 4 * a**2)
    if state == 'plus':
        statevector = np.array([0, -(d1**2 + d3**2), -d2 * d3 - 1j * d1 * d, d1 * d2 - 1j * d3 * d])
        statevector = statevector / np.linalg.norm(statevector)
        print("Initial State is: " + str(statevector))
    elif state == 'minus':
        statevector = np.array([1j * d1, 1j * d3, 1j * d2, 2 * a + D])
        statevector = statevector / np.linalg.norm(statevector)
        print("Initial State is: " + str(statevector))
    else:
        print("Non-valid initial state")
    qml.templates.AmplitudeEmbedding(statevector, wires=[0,1], normalize=True)
