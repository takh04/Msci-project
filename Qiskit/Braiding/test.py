from qiskit import *
import numpy as np
from qiskit.quantum_info import Statevector

pi = np.pi
QR = QuantumRegister(2)
QC = QuantumCircuit(QR)

QC.h(0)
QC.x(0)
QC.cu(pi, -pi / 4, -3/4 * pi, 0, 0, 1)
QC.x(0)
QC.cu(pi, pi / 4, 3/4 * pi, 0, 0, 1)
st = np.array(Statevector.from_instruction(QC))
print(st.reshape(4,1))
print(QC.draw())