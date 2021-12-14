import pennylane as qml
import pennylane.numpy as np

def Coupling_strength(t, tau, d_min, d_max, parameter_path, system):
    if system == 'Beenakker':
        d1 ,d2, d3 = Coupling_strength_Beenakker(t, tau, d_min, d_max, parameter_path)
    elif system == 'Stenger':
        d1, d2, d3 = Coupling_strength_Stenger(t, tau, d_min, d_max, parameter_path)
    return d1, d2, d3

def Coupling_strength_Beenakker(t, tau, d_min, d_max, parameter_path):
    # Cubic path in a parameter space
    if parameter_path == 'cube':
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

    # tetrahedral path in a parameter space
    elif parameter_path == 'tetrahedron':
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


def Coupling_strength_Stenger(t, tau, d_min, d_max, parameter_path):
    # tetrahedral path in parameter space
    if parameter_path == 'tetrahedron':
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

def Hamiltonian(t, tau, d_min, d_max, parameter_path, system):
    d1, d2, d3 = Coupling_strength(t, tau, d_min, d_max, parameter_path, system)

    if system == 'Beenaker':
        H = qml.Hamiltonian(
            [-d3, -d2, d1],
            [qml.Identity(0) @ qml.PauliZ(1), qml.PauliX(0) @ qml.PauliX(1), qml.PauliY(0) @ qml.PauliX(1)])
    elif system == 'Stenger':
        H = qml.Hamiltonian(
            [],
            []
        )
    return H