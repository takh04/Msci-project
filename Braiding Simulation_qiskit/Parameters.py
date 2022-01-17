# This module contains the parameters used during the simulation
"""
This module contains the parameters used during the simulation
d_max, d_min : maximum / minimum coupling strength between MZMs of different wires
a : coupling strength between MZMs of same wires
tau : time to execute a single step of Braiding
N : number of discrete steps for evolving a single step of Braiding (evolving tau)
parameter_path : path taken in a parameter space (d1, d2, d3) during evolution
system: system (Hamiltonian) to simulate
initial_state: initially prepared state. usually even or odd parity ground state of the Hamiltonian.
"""

d_max, d_min = 0.99, 0.01
a = 3
tau = 1
N = 1
parameter_path = 'tetrahedron'
system = 'Stenger'
initial_state = 'odd'