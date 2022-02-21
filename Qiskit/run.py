from qiskit import *
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.visualization import plot_state_qsphere, plot_histogram
from qiskit.quantum_info.operators import Operator, Pauli
from qiskit import IBMQ
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager
from qiskit.tools import job_monitor
import numpy as np
import Parameters
import Simulate

a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state
real_device = False
phase_estimation = True
save_circuit_diagram = False

if real_device:
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q', group='open')
    backend = provider.get_backend('ibmq_bogota')
else:
    backend = Aer.get_backend("aer_simulator")
circuit = Simulate.circuit(phase_estimation=phase_estimation)
transpiled_circuit = transpile(circuit, backend=backend)

if save_circuit_diagram:
    print(circuit.draw(output='mpl', filename='result/circuit.png'))
    print(transpiled_circuit.draw(output='mpl', filename='result/transpiled_circuit.png'))

# Run
num_shot = 1024
job = backend.run(transpiled_circuit, num_shot=num_shot)

# Results
result = job.result()
counts = result.get_counts()
print(counts)

if phase_estimation:
    p0, p1 = counts['0'] / num_shot, counts['1'] / num_shot
    phase = np.arccos(p0 - p1)
    print("Total Phase: ", phase)