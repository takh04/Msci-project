import pennylane as qml
from pennylane import numpy as np
import Evolution
import Initialize
import Parameters
import Hamiltonian

a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state

if system == 'Beenakker':
    dev = qml.device('default.qubit', wires=1)
elif system == 'Stenger':
    dev = qml.device('default.qubit', wires=2)

@qml.qnode(dev)
def simulate():
    if parameter_path == 'cube':
        period_num = 6
    elif parameter_path == 'tetrahedron':
        period_num = 3

    Initialize.initialize()

    dt = tau / N
    loops = 2
    for loop in range(loops):
        t = 0
        for i in range(period_num):
            for i in range(N):
                #print("t: " + str(t))
                Evolution.Evolution(t)
                t = t + dt
    return qml.state()

def dynamic_phase():
    steps = 100
    dt = 6 / steps
    t, gamma_dyn = 0, 0
    for i in range(steps):
        d1, d2, d3 = Hamiltonian.Coupling_strength(t)
        d = np.sqrt(d1**2 + d2**2 + d3**2)
        gamma_dyn = gamma_dyn + d * dt   #ground state energy is -d. There is overall - sign.
        t = t + dt

    return t

def state_initial():
    d1, d2, d3 = d_min, d_min, d_max
    d = (d1**2 + d2**2 + d3**2)**(1/2)

    # Even and Odd ground state
    statevector_even = np.array([1j * (d + d3), d1 + 1j * d2])
    statevector_even = statevector_even / np.linalg.norm(statevector_even)
    statevector_odd = np.array([1j * (d - d3), d1 + 1j * d2])
    statevector_odd = statevector_odd / np.linalg.norm(statevector_odd)

    if initial_state == 'even':
        state_initial = statevector_even
    elif initial_state == 'odd':
        state_initial = statevector_odd
    return state_initial

print("Initial state is " +str(initial_state))
state_final = simulate()
state_initial = state_initial()
relative_phase = state_final / state_initial
print("Final state is: \n " +str(np.reshape(state_final,(len(state_final),1))))
print("Relative Phase is: \n " +str(np.reshape(relative_phase,(len(relative_phase),1))))




