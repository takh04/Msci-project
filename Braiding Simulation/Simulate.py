import pennylane as qml
import Evolution
import initialize


d_max, d_min = 0.99, 0.01
tau = 1
N = 100
dt = tau / N

dev1 = qml.device('default.qubit', wires=2)
@qml.qnode(dev1)
def circuit(parameter_path):
    if parameter_path == 'cube':
        period_num = 6
    elif parameter_path == 'tetrahedron':
        period_num = 3

    initialize('minus')

    t = 0
    for i in range(period_num):
        for i in range(N):
            # print("t: " + str(t))
            Evolution.Evolution_(t, dt, parameter_path)
            t = t + dt
    return qml.state()