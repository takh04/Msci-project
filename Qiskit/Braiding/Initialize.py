"""
This module initializes the initial eigenstates of the system. Possible initial states are,
4MZM: 'even ground', 'odd ground', 'even e1', 'odd e1'
6MZM: 'even ground', 'even e2', 'odd e1', 'odd e3'
Uncoverd states have trivial berry phases.
"""
import Parameters
import numpy as np

a, d_min, d_max = Parameters.a, Parameters.d_min, Parameters.d_max
system, initial_state = Parameters.system, Parameters.initial_state

def initialize(circuit, qubit):
    if system == '4MZM':
        initialize_4MZM(circuit, qubit)
    elif system == '6MZM':
        initialize_6MZM(circuit, qubit)

def initialize_4MZM(circuit, qubit):
    d1, d2, d3 = d_min, d_min, d_max
    d = (d1**2 + d2**2 + d3**2)**(1/2)

    # Even and Odd ground states
    state_even_g = np.array([1j * (-d3 + d), d1 - 1j * d2])
    state_even_g = state_even_g / np.linalg.norm(state_even_g)
    state_odd_g = np.array([1j * (-d3 + d), d1 + 1j * d2])
    state_odd_g = state_odd_g / np.linalg.norm(state_odd_g)

    # Even and Odd excited states
    state_even_e1 = np.array([-1j * (d3 + d), d1 - 1j * d2])
    state_even_e1 = state_even_e1 / np.linalg.norm(state_even_e1)
    state_odd_e1 = np.array([-1j * (d3 + d), d1 + 1j * d2])
    state_odd_e1 = state_odd_e1 / np.linalg.norm(state_odd_e1)


    if initial_state == 'even g':
        statevector = state_even_g
    elif initial_state == 'odd g':
        statevector = state_odd_g
    elif initial_state == 'even e1':
        statevector = state_even_e1
    elif initial_state == 'odd e1':
        statevector = state_odd_e1

    print("Initial State is: \n" + str(np.reshape(statevector, (2, 1))))
    circuit.initialize(statevector, qubit)


def initialize_6MZM(circuit, qubit):
    d1, d2, d3 = d_min, d_min, d_max
    d = (d1**2 + d2**2 + d3**2)**(1/2)
    D = (d1**2 + d2**2 + d3**2 + 4)**(1/2)

    state_even_g = np.array([0, d2 * d3 + 1j * d1 * d, -d1 ** 2 - d3 ** 2, d1 * d2 - 1j * d3 * d])
    state_even_e1 = np.array([1j * (-2 + D), d3, d2, d1])
    state_even_e2 = np.array([0, d2 * d3 - 1j * d1 * d, -d1 ** 2 - d3 ** 2, d1 * d2 + 1j * d3 * d])
    state_even_e3 = np.array([-1j * (2 + D), d3, d2, d1])

    state_odd_g = np.array([1j * d1, 1j * d2, -1j * d3, 2 + D])
    state_odd_e1 = np.array([-d1 * d2 + 1j * d3 * d, d1**2 + d3**2, d2 * d3 + 1j * d1 * d, 0])
    state_odd_e2 = np.array([-1j * d1, -1j * d2, 1j * d3, -2 + D])
    state_odd_e3 = np.array([-d1 * d2 - 1j * d3 * d, d1**2 + d3**2, d2 * d3 - 1j * d1 * d, 0])

    state_even_g = state_even_g / np.linalg.norm(state_even_g)
    state_even_e1 = state_even_e1 / np.linalg.norm(state_even_e1)
    state_even_e2 = state_even_e2 / np.linalg.norm(state_even_e2)
    state_even_e3 = state_even_e3 / np.linalg.norm(state_even_e3)

    state_odd_g = state_odd_g / np.linalg.norm(state_odd_g)
    state_odd_e1 = state_odd_e1 / np.linalg.norm(state_odd_e1)
    state_odd_e2 = state_odd_e2 / np.linalg.norm(state_odd_e2)
    state_odd_e3 = state_odd_e3 / np.linalg.norm(state_odd_e3)

    amplitudes = Parameters.amplitudes
    fullstate_even_g = np.array([0, 0, 0, d1 * d2 - 1j * d3 * d, 0, d2 * d3 + 1j * d1 * d, -d1 ** 2 - d3 ** 2, 0])
    fullstate_odd_g = np.array([0, 1j * d2, -1j * d3, 0, 1j * d1, 0, 0, 2 + D])
    fullstate_even_g = fullstate_even_g / np.linalg.norm(fullstate_even_g)
    fullstate_odd_g = fullstate_odd_g / np.linalg.norm(fullstate_odd_g)
    fullstate = amplitudes[0] * fullstate_even_g + amplitudes[1] * fullstate_odd_g
    fullstate = fullstate / np.linalg.norm(fullstate)


    if initial_state == 'even g':
        statevector = state_even_g
    elif initial_state == 'even e1':
        statevector = state_even_e1
    elif initial_state == 'even e2':
        statevector = state_even_e2
    elif initial_state == 'even e3':
        statevector = state_even_e3
    elif initial_state == 'odd g':
        statevector = state_odd_g
    elif initial_state == 'odd e1':
        statevector = state_odd_e1
    elif initial_state == 'odd e2':
        statevector = state_odd_e2
    elif initial_state == 'odd e3':
        statevector = state_odd_e3
    elif initial_state == 'even + odd':
        statevector = fullstate

    print("Initial State is: \n" + str(np.reshape(statevector, (len(statevector), 1))))
    circuit.initialize(statevector, qubit)












