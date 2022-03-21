from qiskit import *
import numpy as np
import Evolution

v, w = 1, 1
def Hamiltonian(k):
    H = {"X": v + w * np.cos(k), "Y": w * np.sin(k)}
    return H
