"""
This module simulates a Quantum Dynamics of Majorana Zero Modes (MZM) Braiding.
Parameters of the simulation can be controlled in module Parameter.py.
To use real quantum device for simulation, the user must save and load their own IBMQ account.
Saving statevector is only possible with classical simulation, hence must be commented out with real device.
"""
from qiskit import *
import Parameters
import Hamiltonian
import Initialize
import Evolution
from qiskit.quantum_info import Statevector
import numpy as np

# Parameters Used
parameter_path, system, loops, initial_state = Parameters.parameter_path, Parameters.system, Parameters.loops, Parameters.initial_state
initial_state_even = ["even g", "even e1", "even e2", "even e3"]
initial_state_odd = ["odd g", "odd e1", "odd e2", "odd e3"]
# Number of legs in Parameter space
if parameter_path == 'cube':
    legs = 6
elif parameter_path == 'tetrahedron':
    legs = 3

# Number of qubits
if system == '4MZM':
    n = 1
elif system == '6MZM':
    n = 2


def circuit(tau, N, phase_estimation=False, statevector=False, proj_meas=False, params=[0,0]):

    dt = tau / N
    def unitary_evolution(QC):
        for loop in range(loops):
            t = 0
            for i in range(legs):
                for j in range(N):
                    H, H_even, H_odd = Hamiltonian.Hamiltonian(t, tau)
                    if proj_meas:
                        H = H
                        circuit = Evolution.hamiltonian_simulation(H, qbit, t=dt)
                    elif phase_estimation:
                        H = H_even if initial_state in initial_state_even else H_odd
                        circuit = Evolution.hamiltonian_simulation(H, qbit, control_qubit=ctrlbit[0], t=dt)
                    elif statevector:
                        H = H_even if initial_state in initial_state_even else H_odd
                        circuit = Evolution.hamiltonian_simulation(H, qbit, t=dt)
                    QC += circuit
                    t += dt

    if statevector:
        qbit = QuantumRegister(n, 'q')
        QC = QuantumCircuit(qbit)               # Define a Quantum Circuit
        Initialize.initialize(QC, qbit)         # Initial state initialization
        unitary_evolution(QC)                   # Unitary Evolution
        st = Statevector.from_instruction(QC)
        return st

    elif phase_estimation:
        qbit, ctrlbit, cbit = QuantumRegister(n, 'q'), QuantumRegister(1, 'control'), ClassicalRegister(1, 'c')
        QC = QuantumCircuit(ctrlbit, qbit, cbit)        # Define a Quantum Circuit
        QC.h(ctrlbit)                                   # Hadamard on control qubit
        QC.barrier()
        Initialize.initialize(QC, qbit)                 # Initial state initialization
        unitary_evolution(QC)                           # Unitary Evolution
        QC.barrier()
        QC.h(ctrlbit)                                   # Hadamard on control qubit
        QC.measure(ctrlbit, cbit)                       # measure control qubit
        return QC

    elif proj_meas:
        qbit, cbit = QuantumRegister(n + 1, 'q'), ClassicalRegister(1, 'c')
        QC = QuantumCircuit(qbit, cbit)
        QC.rx(params[0], qbit[1])
        QC.ry(params[1], qbit[1])
        QC.x(qbit[0])
        QC.x(qbit[1])
        unitary_evolution(QC)
        QC.x(qbit[0])
        QC.x(qbit[1])
        QC.rz(-np.pi / 2, qbit[1])
        QC.ry(-params[1], qbit[1])
        QC.rx(-params[0], qbit[1])
        QC.measure(qbit[1], cbit)
        return QC







