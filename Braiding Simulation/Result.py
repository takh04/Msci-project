import Simulate

d_max, d_min = 0.99, 0.01
tau = 1
N = 10
parameter_path = 'cube'
system = 'Beenakker'
state = 'minus'
probs = Simulate.circuit(tau, d_min, d_max, parameter_path, system, N, state)
print(probs)