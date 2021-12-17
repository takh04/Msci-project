import pennylane as qml
import Hamiltonian
import Parameters

a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state

def Evolution(t):
    dt = tau / N
    if system == 'Beenakker':
        H = Hamiltonian.Hamiltonian(t)
        qml.templates.ApproxTimeEvolution(H, dt, 1)
    elif system == 'Stenger':
        Heven, Hodd = Hamiltonian.Hamiltonian(t)
        if initial_state == 'even':
            qml.templates.ApproxTimeEvolution(Heven, dt, 1)
        elif initial_state == 'odd':
            qml.templates.ApproxTimeEvolution(Hodd, dt, 1)
