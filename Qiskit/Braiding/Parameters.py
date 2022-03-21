# This module contains the parameters used during the simulation
"""
This module contains the parameters used during the simulation
d_max, d_min : maximum / minimum coupling strength between MZMs of different wires
a : coupling strength between MZMs of same wires
parameter_path : path taken in a parameter space (d1, d2, d3) during evolution
system: system (Hamiltonian) to simulate
initial_state: initially prepared state. usually even or odd parity ground state of the Hamiltonian.
loops = number of loops taken in the parameter space
"""
# Simulation Type
real_device = False
phase_estimation = False
statevector = True
proj_meas = False


# Simulation Parameters
d_min = 0.0001
d_max = 0.9999
a = 1
parameter_path = 'cube'
system = '6MZM'
initial_state = 'odd e1'
loops = 1


