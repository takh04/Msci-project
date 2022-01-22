import Parameters
import numpy as np

a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state

def initialize(circuit, qubit):
    if system == 'Beenakker':
        initialize_Beenakker(circuit, qubit)
    elif system == 'Stenger':
        initialize_Stenger(circuit, qubit)

def initialize_Beenakker(circuit, qubit):
    d1, d2, d3 = d_min, d_min, d_max
    d = (d1**2 + d2**2 + d3**2)**(1/2)

    # Even and Odd ground state
    statevector_even = np.array([1j * (d + d3), d1 + 1j * d2])
    statevector_even = statevector_even / np.linalg.norm(statevector_even)
    statevector_odd = np.array([1j * (d - d3), d1 + 1j * d2])
    statevector_odd = statevector_odd / np.linalg.norm(statevector_odd)

    if initial_state == 'even':
        statevector = statevector_even
        print("Initial State is: \n" + str(np.reshape(statevector_even, (2, 1))))

    elif initial_state == 'odd':
        statevector = statevector_odd
        print("Initial State is: \n" + str(np.reshape(statevector_odd, (2, 1))))
    else:
        print("Non-valid initial state")
    circuit.initialize(statevector, qubit)


def initialize_Stenger(circuit, qubit):
    d1, d2, d3 = d_max, d_min, d_min
    d = (d1**2 + d2**2 + d3**2)**(1/2)
    D = (d1**2 + d2**2 + d3**2 + 4 * a**2)
    if initial_state == 'even':
        statevector = np.array([0, -(d1**2 + d3**2), d2 * d3 + 1j * d1 * d, d1 * d2 - 1j * d3 * d])
        statevector = statevector / np.linalg.norm(statevector)
        print("Initial State is: \n" + str(np.reshape(statevector, (4, 1))))
    elif initial_state == 'odd':
        statevector = np.array([1j * d1, 1j * d3, 1j * d2, 2 * a + D])
        statevector = statevector / np.linalg.norm(statevector)
        print("Initial State is: \n" + str(np.reshape(statevector, (4, 1))))
    else:
        print("Non-valid initial state")
    circuit.initialize(statevector, qubit)
