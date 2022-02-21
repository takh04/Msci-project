import pennylane as qml
from pennylane import numpy as np

def toric_hamiltonian(A, B, M, N):
    # Toric code of dimenstion M * N (Total 2 * N * M qubits)
    coeffs, obs = [], []
    for i in range(M):
        for j in range(N):
            # Vertex operator
            v_right = 'q' + str(i) + ',' + str(j)
            v_left = 'q' + str(i) + ',' + str(j - 1)
            v_top = 'q' + str(i - 1) + ',' + str(j + N)
            v_bottom = 'q' + str(i) + ',' + str(j + N)
            if i == 0:
                v_top = 'q' + str(M - 1) + ',' + str(j + N)
            if j == 0:
                v_left = 'q' + str(i) + ',' + str(N - 1)

            # Plaqutte operator
            p_top = 'q' + str(i) + ',' + str(j)
            p_right = 'q' + str(i) + ',' + str(j + N + 1)
            p_bottom = 'q' + str(i + 1) + ',' + str(j)
            p_left = 'q' + str(i) + ',' + str(j + N)
            if j == N-1:
                p_right = 'q' + str(i) + ',' + str(N)
            if i == M-1:
                p_bottom = 'q' + str(0) + ',' + str(j)

            coeffs.append(-A)
            coeffs.append(-B)
            obs.append(qml.PauliZ(v_right) @ qml.PauliZ(v_left) @ qml.PauliZ(v_top) @ qml.PauliZ(v_bottom))
            obs.append(qml.PauliX(p_right) @ qml.PauliX(p_left) @ qml.PauliX(p_top) @ qml.PauliX(p_bottom))
    H = qml.Hamiltonian(coeffs, obs)
    return H


def toric_ground_state(M,N):
    for n in range(N):
        for m in range(M):
            qubit = 'q' + str(n) + ',' + str(m)
            qml.Hadamard(qubit)

    for n in range(N):
        for m in range(M):
            qubit1 = 'q' + str(n) + ',' + str(m)
            qubit2 = 'q' + str(n) + ',' + str(m+N)
            qml.CNOT(wires=[qubit1, qubit2])

    for n in range(N):
        for m in range(M):
            qubit1 = 'q' + str(n) + ',' + str(m)
            qubit2 = 'q' + str(n) + ',' + str(m + N + 1)
            if m + N + 1 == 2 * N:
                qubit2 = 'q' + str(n) + ',' + str(N)
            qml.CNOT(wires=[qubit1, qubit2])

    for n in range(N):
        for m in range(M):
            qubit1 = 'q' + str(n) + ',' + str(m + N)
            qubit2 = 'q' + str(n + 1) + ',' + str(m)
            if n + 1 == M:
                qubit2 = 'q' + str(0) + ',' + str(m)
            qml.CNOT(wires=[qubit1, qubit2])


def toric_code_mixedBC(A, B, dimension):

    if dimension == '3by3':
        qubits = 9
        coeffs = [-A, -A, -A, -A, -B, -B, -B, -B] # A for Vertex (Blue), B for Plaqutte (Purple)
        ops = [qml.PauliX(1) @ qml.PauliX(2) @ qml.PauliX(4) @qml.PauliX(5),
               qml.PauliX(3) @ qml.PauliX(4) @ qml.PauliX(6) @qml.PauliX(7),
               qml.PauliX(0) @ qml.PauliX(3),
               qml.PauliX(5) @ qml.PauliX(8),
               qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(3) @qml.PauliZ(4),
               qml.PauliZ(4) @ qml.PauliZ(5) @ qml.PauliZ(7) @qml.PauliZ(8),
               qml.PauliZ(1) @ qml.PauliZ(2),
               qml.PauliZ(6) @ qml.PauliZ(7)]
        H = qml.Hamiltonian(coeffs, ops)

    if dimension == '5by5':
        qubits = 25
        coeffs = [-A, -A, -A, -A, -A, -A, -A, -A, -A, -A, -A, -A,
                  -B, -B, -B, -B, -B, -B, -B, -B, -B, -B, -B, -B]
        ops = [qml.PauliX(1) @ qml.PauliX(2) @ qml.PauliX(6) @qml.PauliX(7),
               qml.PauliX(3) @ qml.PauliX(4) @ qml.PauliX(8) @ qml.PauliX(9),
               qml.PauliX(5) @ qml.PauliX(6) @ qml.PauliX(10) @ qml.PauliX(11),
               qml.PauliX(7) @ qml.PauliX(8) @ qml.PauliX(12) @ qml.PauliX(13),
               qml.PauliX(11) @ qml.PauliX(12) @ qml.PauliX(16) @ qml.PauliX(17),
               qml.PauliX(13) @ qml.PauliX(14) @ qml.PauliX(18) @ qml.PauliX(19),
               qml.PauliX(15) @ qml.PauliX(16) @ qml.PauliX(20) @ qml.PauliX(21),
               qml.PauliX(17) @ qml.PauliX(18) @ qml.PauliX(22) @ qml.PauliX(23),
               qml.PauliX(0) @ qml.PauliX(5),
               qml.PauliX(10) @ qml.PauliX(15),
               qml.PauliX(9) @ qml.PauliX(14),
               qml.PauliX(19) @ qml.PauliX(24),

               qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(5) @ qml.PauliZ(6),
               qml.PauliZ(2) @ qml.PauliZ(3) @ qml.PauliZ(7) @ qml.PauliZ(8),
               qml.PauliZ(6) @ qml.PauliZ(7) @ qml.PauliZ(11) @ qml.PauliZ(12),
               qml.PauliZ(8) @ qml.PauliZ(9) @ qml.PauliZ(13) @ qml.PauliZ(14),
               qml.PauliZ(10) @ qml.PauliZ(11) @ qml.PauliZ(15) @ qml.PauliZ(16),
               qml.PauliZ(12) @ qml.PauliZ(13) @ qml.PauliZ(17) @ qml.PauliZ(18),
               qml.PauliZ(16) @ qml.PauliZ(17) @ qml.PauliZ(21) @ qml.PauliZ(22),
               qml.PauliZ(18) @ qml.PauliZ(19) @ qml.PauliZ(23) @ qml.PauliZ(24),
               qml.PauliZ(1) @ qml.PauliZ(2),
               qml.PauliZ(3) @ qml.PauliZ(4),
               qml.PauliZ(20) @ qml.PauliZ(21),
               qml.PauliZ(22) @ qml.PauliZ(23)]
        H = qml.Hamiltonian(coeffs, ops)
    return qubits, H

def toric_ground_mixedBC(dimension):

    if dimension == '3by3':
        qml.Hadamard(0)
        qml.Hadamard(2)
        qml.Hadamard(5)
        qml.Hadamard(6)

        qml.CNOT(wires=[0, 3])
        qml.CNOT(wires=[5, 8])

        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[5, 4])
        qml.CNOT(wires=[6, 7])

        qml.CNOT(wires=[2, 1])
        qml.CNOT(wires=[3, 4])
        qml.CNOT(wires=[8, 7])





