"""
This module generates the time dependent Hamiltonian at given time. system and initial_state is considered.
system: determines the system to gain Hamiltonian from
initial_state: the program simulates even and odd parity hamiltonian separately. initial_state determines the parity.
"""
import Parameters

a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state


def C_strength(t):
    # Interaction strength between MZMs at given time
    # For 4MZM: d1,d2,d3 = J01, J02, J03
    # For 6MZM: d1,d2,d3 = J01, J12, J20
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


def Hamiltonian(t):
    d1, d2, d3 = C_strength(t)
    if system == '4MZM':
        Heven = {"X": d2, "Y": d1, "Z": d3}
        Hodd = {"X": -d2, "Y": d1, "Z": d3}
    elif system == '6MZM':
        Heven = {"ZZ": a, "IZ": a, "ZI": a, "XY": d1, "ZY": d2, "YI": d3}
        Hodd = {"ZZ": -a, "IZ": a, "ZI": a, "YX": d1, "IY": d2, "YZ": -d3}

    if initial_state == 'even':
        return Heven
    elif initial_state == 'odd':
        return Hodd
