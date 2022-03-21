from qiskit import *
from qiskit.visualization import plot_state_qsphere, plot_histogram
from qiskit import IBMQ
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager
from qiskit.providers.ibmq import least_busy
from qiskit.tools import job_monitor
import numpy as np
import Simulate
import Parameters
import matplotlib.pyplot as plt

real_device = Parameters.real_device
phase_estimation = Parameters.phase_estimation
statevector = Parameters.statevector
proj_meas = Parameters.proj_meas

save_circuit_diagram = False
save_simulation_result = False

def run(tau, N, params=[0,0]):
    if statevector:
        st = Simulate.circuit(tau, N, phase_estimation, statevector, proj_meas)
        if save_simulation_result:
            f = open("result/N= " + str(N) + " tau= " + str(tau) + " Init= " + str(Parameters.initial_state) + ".txt", "a")
            f.write("dmin, dmax = " + str(Parameters.d_min) + ", " + str(Parameters.d_max) + "\n")
            f.write("N = " + str(N) + "\n")
            f.write("tau = " + str(tau) + "\n")
            f.write("Initial State = " + str(Parameters.initial_state) + "\n")
            f.write("Final State = " + str(st))
        return st

    else:
        if real_device:
            IBMQ.load_account()
            provider = IBMQ.get_provider(hub='ibm-q', group='open')
            #backend = provider.get_backend('ibmq_bogota')
            backends = provider.backends(filters=lambda x: x.configuration().n_qubits > 1
                                                                and not x.configuration().simulator)
            backend = least_busy(backends)
        else:
            backend = Aer.get_backend("aer_simulator")


        circuit = Simulate.circuit(tau, N, phase_estimation, statevector, proj_meas, params=params)
        transpiled_circuit = transpile(circuit, backend=backend)

        if save_circuit_diagram:
            print(circuit.draw(output='mpl', filename='result/circuit.png'))
            print(transpiled_circuit.draw(output='mpl', filename='result/transpiled_circuit.png'))

        # Run
        num_shot = 1024
        job = backend.run(transpiled_circuit, num_shot=num_shot)
        job_monitor(job)

        # Results
        result = job.result()
        counts = result.get_counts()
        print(counts)

        if phase_estimation:
            p0, p1 = counts['0'] / num_shot, counts['1'] / num_shot
            phase = np.arccos(p0 - p1)
            print("Total Phase: ", phase)

