from qiskit import *
import numpy as np
import Parameters
import Initialize
import Hamiltonian
import Evolution
from qiskit.quantum_info import Statevector
a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state
if system == '4MZM':
    n = 1
elif system == '6MZM':
    n = 2
legs = 6

quantum_bit = QuantumRegister(n,'q')
classcial_bit = ClassicalRegister(n, 'c')
QC = QuantumCircuit(quantum_bit, classcial_bit)

Initialize.initialize(QC, quantum_bit)
dt = tau / N
t = 0
for i in range(legs):
    for j in range(N):
        H = Hamiltonian.Hamiltonian(t)
        circuit = Evolution.hamiltonian_simulation(H, quantum_bit, t=dt)
        QC = QC + circuit
        t = t + dt
st0 = Statevector.from_instruction(QC)
print(str(np.reshape(st0, (4, 1))))

f = open("result/N= " + str(N) + " tau= " + str(tau) + " Init= " + str(initial_state) + ".txt", "a")
f.write("dmin, dmax = " + str(d_min) + ", " + str(d_max))
f.write("\n")
f.write("N = " + str(N))
f.write("\n")
f.write("tau = " + str(tau))
f.write("\n")
f.write("Initial State = " + str(initial_state))
f.write("\n")
f.write("Final State = " + str(st0))


