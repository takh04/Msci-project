"""
This module generates the time dependent Hamiltonian at given time. system and initial_state is considered.
system: determines the system to gain Hamiltonian from
initial_state: the program simulates even and odd parity hamiltonian separately. initial_state determines the parity.
"""
import Parameters

a, d_min, d_max = Parameters.a, Parameters.d_min, Parameters.d_max
parameter_path, system = Parameters.parameter_path, Parameters.system


def C_strength(t, tau):
    """
    :param t: interested time t
    :param tau: period / time the system takes to evolve through 1 leg in parameter space
    :return: coupling strength at time t for a system with period tau
    For 4MZM: d1,d2,d3 = J01, J02, J03
    For 6MZM: d1,d2,d3 = J01, J12, J20
    """
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


def Hamiltonian(t, tau):
    """
    :param t: interested time t
    :param tau: period / time system takes to evolve through 1 leg in parameter space
    :return: Hamiltonian of the even and odd parity states at time t.
    H_proj is added, which is a Hamiltonian for the combined system.
    """
    d1, d2, d3 = C_strength(t, tau)
    if system == '4MZM':
        H_even = {"X": d2, "Y": d1, "Z": d3}
        H_odd = {"X": -d2, "Y": d1, "Z": d3}
        H = {"ZI": d3, "YX": d1, "YY": -d2}

    elif system == '6MZM':
        H_even = {"ZZ": a, "IZ": a, "ZI": a, "YX": d1, "IY": d2, "YZ": d3}
        H_odd = {"ZZ": -a, "IZ": a, "ZI": a, "YX": d1, "IY": d2, "YZ": d3}
        H = {"ZII": a, "IZI": a, "IIZ": a, "YXI": d1, "IYX": d2, "YZX": d3}

    initial_state_even = ["even g", "even e1", "even e2", "even e3"]
    initial_state_odd = ["odd g", "odd e1", "odd e2", "odd e3"]
    if Parameters.initial_state in initial_state_even:
        return H_even
    elif Parameters.initial_state in initial_state_odd:
        return H_odd
    else:
        return H

