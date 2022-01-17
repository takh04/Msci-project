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

def circuit():
    if parameter_path == 'cube':
        period_num = 6
    elif parameter_path == 'tetrahedron':
        period_num = 3

    if system == 'Beenakker':
        n = 1
    elif system == 'Stenger':
        n = 2

    QC = QuantumCircuit(n,n)
    quantum_register = QuantumRegister(n, 'q')
    Initialize.initialize(QC)

    dt = tau / N
    loops = 1
    for loop in range(loops):
        t = 0
        for i in range(period_num):
            for i in range(N):
                # print("t: " + str(t))
                H = Hamiltonian.Hamiltonian(t)
                circuit = Evolution.hamiltonian_simulation(H, quantum_register, t=dt)
                QC = QC + circuit
                t = t + dt
    QC.measure_all()
    #Save statevector is only possible on classical simulator. It is impossible for real device or noisy model.
    #QC.save_statevector(label='my_sv')
    print(QC.draw(output='text'))
    return QC


IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open')
backend = provider.get_backend('ibmq_bogota')
backend_sim = Aer.get_backend("aer_simulator")

circuit = circuit()
transpiled_circuit = transpile(circuit, backend=backend)
print(transpiled_circuit.draw())
qobj = assemble(transpiled_circuit)
job = backend.run(qobj)
result = job.result()
counts = result.get_counts()
print(counts)
print(result.data(0))
