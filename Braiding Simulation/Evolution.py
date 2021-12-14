import pennylane as qml
import Hamiltonian

def Evolution(t, tau, d_min, d_max, parameter_path, system, dt):
    H = Hamiltonian.Hamiltonian(t, tau, d_min, d_max, parameter_path, system)
    qml.templates.ApproxTimeEvolution(H, dt, 1)
