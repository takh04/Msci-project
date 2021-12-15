import pennylane as qml
import Evolution
import Initialize

dev1 = qml.device('default.qubit', wires=2)
@qml.qnode(dev1)
def circuit(tau, d_min, d_max, parameter_path, system, dt, state):
    if parameter_path == 'cube':
        period_num = 6
    elif parameter_path == 'tetrahedron':
        period_num = 3

    Initialize.initialize(state, d_min, d_max, system)

    for k in range(2):
        t = 0
        for i in range(period_num):
            for i in range(N):
                #print("t: " + str(t))
                Evolution.Evolution(t, tau, d_min, d_max, parameter_path, system, dt)
                t = t + dt
    return qml.state()
