import pennylane as qml
from pennylane import numpy as np

def VQE():
    layers = 3
    params = np.random.randn(layers, qubits, 3)

    def circuit(params):
        for layer in range(layers):
            for qubit in range(qubits):
                qml.Rot(params[layer][qubit][0], params[layer][qubit][1], params[layer][qubit][2], wires=qubit)
            for qubit in range(qubits - 1):
                qml.CNOT(wires=[qubit, qubit + 1])
            qml.CNOT(wires=[qubits - 1, 0])

    @qml.qnode(dev)
    def cost_fn(params, state=False):
        circuit(params)
        if state:
            return qml.state()
        else:
            return qml.expval(H)

    opt = qml.NesterovMomentumOptimizer(0.1)
    steps = 1
    for step in range(steps):
        params, prev_energy = opt.step_and_cost(cost_fn, params)
        current_energy = cost_fn(params)
        print("step " + str(step) + ": " + str(current_energy))

    print("params: " + str(params))
    print("state:  " + str(cost_fn(params, state=True)))
