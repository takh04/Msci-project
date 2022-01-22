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

a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state


def circuit(phase_estimation=False):

    # Hamiltonian Path
    if parameter_path == 'cube':
        period_num = 6
    elif parameter_path == 'tetrahedron':
        period_num = 3
    # Number of qubits
    if system == 'Beenakker':
        n = 1
    elif system == 'Stenger':
        n = 2

    # Quantum Circuit Initialization
    quantum_bit = QuantumRegister(n, 'q')
    classical_bit = ClassicalRegister(1, 'c')
    if phase_estimation:
        control_bit = QuantumCircuit(1, 'control')
        QC = QuantumCircuit(control_bit, quantum_bit, classical_bit)
    else:
        control_bit = None
        QC = QuantumCircuit(quantum_bit, classical_bit)

    if control_bit is not None:
        QC.h(control_bit)
    Initialize.initialize(QC, quantum_bit)

    dt = tau / N
    loops = 1
    for loop in range(loops):
        t = 0
        for i in range(period_num):
            for i in range(N):
                # print("t: " + str(t))
                H = Hamiltonian.Hamiltonian(t)
                circuit = Evolution.hamiltonian_simulation(H, quantum_bit, control_qubit=control_bit[0], t=dt)
                QC += circuit
                t += dt

    if control_bit is not None:
        QC.h(control_bit)

    if control_bit is None:
        QC.measure_all()
    else:
        QC.measure(control_bit, classical_bit)
    QC.save_statevector(label='my_sv')
    return QC

# load IBM backends
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open')
backend = provider.get_backend('ibmq_bogota')
backend_sim = Aer.get_backend("aer_simulator")

# generate and draw circuit
circuit = circuit(phase_estimation=True)
print(circuit.draw(output='mpl', filename='result/transpiled_circuit.png'))

# circuit transpilation
transpiled_circuit = transpile(circuit, backend=backend_sim)
print(transpiled_circuit.draw(output='mpl', filename='result/transpiled_circuit.png'))

# Run
qobj = assemble(transpiled_circuit)
num_shot = 1024
job = backend_sim.run(qobj, num_shot=num_shot)
result = job.result()
counts = result.get_counts()
print("Measurement Counts: ", counts)
if counts['0'] == num_shot or counts['1'] == num_shot:
    if counts['0'] == num_shot:
        p0, p1 = 1, 0
    else:
        p0, p1 = 0, 1
else:
    p0, p1 = counts['0'] / num_shot, counts['1'] / num_shot
print("Result: ", result.data(0))
phase = np.arccos(p0 - p1)
print("Total Phase: ", phase)
