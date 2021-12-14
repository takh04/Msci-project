import pennylane as qml
from pennylane import numpy as np
import Hamiltonian

def Evolution(t, dt, parameter_path):
    Hamiltonian = Hamiltonian.H(t, parameter_path)
    qml.templates.ApproxTimeEvolution(Hamiltonian, dt, 1)
