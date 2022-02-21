import pennylane as qml
import numpy as np
from qiskit import *


QC = QuantumCircuit(2,1)
QC.h(1)
QC.measure(1,0)
print(QC.draw("text"))

backend = Aer.get_backend("aer_simulator")
qobj = assemble(QC)
job = backend.run(qobj)
result = job.result()
counts = result.get_counts()

print(counts['1'])

print(np.arccos(1))