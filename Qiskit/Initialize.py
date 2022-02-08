"""
This module initializes the initial eigenstates of the system. Possible initial states are,
4MZM: 'even ground', 'odd ground', 'even e1', 'odd e1'
6MZM: 'even ground', 'even e2', 'odd e1', 'odd e3'
Uncoverd states have trivial berry phases.
"""
import Parameters
import numpy as np

a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state

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

    if initial_state == 'even ground':
        statevector = state_even_g
    elif initial_state == 'odd ground':
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
    D = (d1**2 + d2**2 + d3**2 + 4 * a**2)

    # Even Ground State
    state_even_g = np.array([0, -d1 ** 2 - d3 ** 2, d2 * d3 - 1j * d1 * d, d1 * d2 + 1j * d3 * d])
    state_even_g = state_even_g / np.linalg.norm(state_even_g)
    # Even Second Excited State
    state_even_e2 = np.array([0, -d1 ** 2 - d3 ** 2, d2 * d3 + 1j * d1 * d, d1 * d2 - 1j * d3 * d])
    state_even_e2 = state_even_e2 / np.linalg.norm(state_even_e2)
    # Odd First Excited State
    state_odd_e1 = np.array([d1 * d2 + 1j * d3 * d, d2 * d3 - 1j * d1 * d, -d1**2 - d3**2, 0])
    state_odd_e1 = state_odd_e1 / np.linalg.norm(state_odd_e1)
    # Odd Third Excited State
    state_odd_e3 = np.array([d1 * d2 - 1j * d3 * d, d2 * d3 + 1j * d1 * d, -d1**2 - d3**2, 0])
    state_odd_e3 = state_odd_e3 / np.linalg.norm(state_odd_e3)

    if initial_state == 'even ground':
        statevector = state_even_g
    elif initial_state == 'even e2':
        statevector = state_even_e2
    elif initial_state == 'odd e1':
        statevector = state_odd_e1
    elif initial_state == 'odd e3':
        statevector = state_odd_e3

    print("Initial State is: \n" + str(np.reshape(statevector, (4, 1))))
    circuit.initialize(statevector, qubit)
