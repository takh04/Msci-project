"""
This module simulates a Quantum Dynamics of Majorana Zero Modes (MZM) Braiding.
Parameters of the simulation can be controlled in module Parameter.py.
To use real quantum device for simulation, the user must save and load their own IBMQ account.
Saving statevector is only possible with classical simulation, hence must be commented out with real device.
"""

from qiskit import *
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.visualization import plot_state_qsphere, plot_histogram
from qiskit.quantum_info.operators import Operator, Pauli
from qiskit import IBMQ
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager
from qiskit.tools import job_monitor

import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import Parameters
import Hamiltonian
import Initialize
import Evolution

# Parameters Used
a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state
loops = Parameters.loops

# Number of legs in Parameter space
if parameter_path == 'cube':
    period_num = 6
elif parameter_path == 'tetrahedron':
    period_num = 3

# Number of qubits
if system == '4MZM':
    n = 1
elif system == '6MZM':
    n = 2

def circuit(phase_estimation=False):
    # Quantum Circuit Initialization
    quantum_bit = QuantumRegister(n, 'q')
    classical_bit = ClassicalRegister(1, 'c')

    if phase_estimation:
        control_bit = QuantumRegister(1, 'control')
        QC = QuantumCircuit(control_bit, quantum_bit, classical_bit)
        QC.h(control_bit)
        QC.barrier()
    else:
        QC = QuantumCircuit(quantum_bit, classical_bit)
    Initialize.initialize(QC, quantum_bit)

    dt = tau / N
    for loop in range(loops):
        t = 0
        for i in range(period_num):
            for j in range(N):
                H = Hamiltonian.Hamiltonian(t)
                if phase_estimation:
                    circuit = Evolution.hamiltonian_simulation(H, quantum_bit, control_qubit=control_bit[0], t=dt)
                else:
                    circuit = Evolution.hamiltonian_simulation(H, quantum_bit, t=dt)
                QC+= circuit
                t += dt

    if phase_estimation:
        QC.barrier()
        QC.h(control_bit)
        QC.measure(control_bit, classical_bit)
    else:
        QC.measure_all()
    return QC