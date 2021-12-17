import pennylane as qml
from pennylane import numpy as np
import Evolution
import Initialize
import Parameters

a, d_min, d_max, N, tau = Parameters.a, Parameters.d_min, Parameters.d_max, Parameters.N, Parameters.tau
parameter_path, system, initial_state = Parameters.parameter_path, Parameters.system, Parameters.initial_state

dev1 = qml.device('default.qubit', wires=2)
@qml.qnode(dev1)
def simulate():
    if parameter_path == 'cube':
        period_num = 6
    elif parameter_path == 'tetrahedron':
        period_num = 3

    Initialize.initialize()

    dt = tau / N
    for k in range(2):
        t = 0
        for i in range(period_num):
            for i in range(N):
                #print("t: " + str(t))
                Evolution.Evolution(t)
                t = t + dt
    return qml.state()

result = simulate()
print("Final state is: \n " +str(np.reshape(result,(len(result),1))))