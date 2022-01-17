"""
This module generates the time dependent Hamiltonian at given time. system and initial_state is considered.
system: determines the system to gain Hamiltonian from
initial_state: the program simulates even and odd parity hamiltonian separately. initial_state determines the parity.
"""
import Parameters
a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state

def Coupling_strength(t):
    if system == 'Beenakker':
        d1 ,d2, d3 = Coupling_strength_Beenakker(t)
    elif system == 'Stenger':
        d1, d2, d3 = Coupling_strength_Stenger(t)
    return d1, d2, d3

def Coupling_strength_Beenakker(t):
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

def Coupling_strength_Stenger(t):
    # tetrahedral path in parameter space
    # d1 = J01, d2 = J12, d3 = J20
    if parameter_path == 'tetrahedron':
        if t == 0:
            d1, d2, d3 = d_max, d_min, d_min
        elif t < tau:
            d2 = d_min
            d3 = d_min + (d_max - d_min) * t / tau
            d1 = d_max - (d_max - d_min) * t / tau
        elif t < 2 * tau:
            d1 = d_min
            d2 = d_max - (d_max - d_min) * (t - tau) / tau
            d3 = d_min + (d_max - d_min) * (t - tau) / tau
        elif t < 3 * tau:
            d2 = d_min
            d3 = d_max - (d_max - d_min) * (t - 2 * tau) / tau
            d1 = d_min + (d_max - d_min) * (t - 2 * tau) / tau
        elif t == 3 * tau:
            d1, d2, d3 = d_max, d_min, d_min
    return d1, d2, d3

def Hamiltonian(t):
    d1, d2, d3 = Coupling_strength(t)
    if system == 'Beenakker':
        Heven = {"X": -d2, "Y": d1, "Z": -d3}
        Hodd = {"X": -d2, "Y": d1, "Z": d3}
    elif system == 'Stenger':
        Heven = {"ZZ": a, "IZ": a, "ZI": a, "YX": d1, "IY": d2, "YZ": d3}
        Hodd = {"ZZ": -a, "IZ": a, "ZI": a, "YX": d1, "IY": d2, "YZ": -d3}

    if initial_state == 'even':
        return Heven
    elif initial_state == 'odd':
        return Hodd
