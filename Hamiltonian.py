import pennylane as qml
import pennylane.numpy as np

def Coupling_strength_cube(t, tau, d_min, d_max):
    if t == 0:
        d1, d2, d3 = d_min, d_min, d_max
    elif t < tau:
        d1 = d_min + (d_max - d_min) * t / tau
        d2, d3 = d_min, d_max
    elif t < 2 * tau:
        d1, d2 = d_max, d_min
        d3 = d_max - (d_max - d_min) * (t - tau) / tau
    elif t < 3 * tau:
        d1, d3 = d_max, d_min
        d2 = d_min + (d_max - d_min) * (t - 2 * tau) / tau
    elif t < 4 * tau:
        d2, d3 = d_max, d_min
        d1 = d_max - (d_max - d_min) * (t - 3 * tau) / tau
    elif t < 5 * tau:
        d1, d2 = d_min, d_max
        d3 = d_min + (d_max - d_min) * (t - 4 * tau) / tau
    elif t < 6 * tau:
        d1, d3 = d_min, d_max
        d2 = d_max - (d_max - d_min) * (t - 5 * tau) / tau
    elif t == 6 * tau:
        d1, d2, d3 = d_min, d_min, d_max
    return d1, d2, d3

def Coupling_strength_tetrahedron(t, tau, d_min, d_max):
    if t == 0:
        d1, d2, d3 = d_min, d_min, d_max
    elif t < tau:
        d2 = d_min
        d1 = d_min + (d_max - d_min) * t / tau
        d3 = d_max - (d_max - d_min) * t / tau
    elif t < 2 * tau:
        d3 = d_min
        d1 = d_max - (d_max - d_min) * (t - tau) / tau
        d2 = d_min + (d_max - d_min) * (t - tau) / tau
    elif t < 3 * tau:
        d1 = d_min
        d2 = d_max - (d_max - d_min) * (t - 2 * tau) / tau
        d3 = d_min + (d_max - d_min) * (t - 2 * tau) / tau
    elif t == 3 * tau:
        d1, d2, d3 = d_min, d_min, d_max
    return d1, d2, d3

def H(t, parameter_path):
    if parameter_path == 'cube':
        d1, d2, d3 = Coupling_strength_cube(t)
    elif parameter_path == 'tetrahedron':
        d1, d2, d3 = Coupling_strength_tetrahedron(t)
    H = qml.Hamiltonian(
        [-d3, -d2, d1],
        [qml.Identity(0) @ qml.PauliZ(1), qml.PauliX(0) @ qml.PauliX(1), qml.PauliY(0) @ qml.PauliX(1)])
    return H