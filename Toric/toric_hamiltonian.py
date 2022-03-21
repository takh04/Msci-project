import pennylane as qml
from pennylane import numpy as np

def toric_code_hamiltonian(A, B, dimension, BC):
    if BC == 'mixed':
        qubits, H = toric_code_mixedBC(A, B, dimension)
    elif BC == 'matching':
        qubits, H = toric_code_matchingBC(A, B, dimension)
    return qubits, H

def toric_code_ground(dimension, BC, logical_state, theta):
    if BC == 'mixed':
        toric_ground_mixedBC(dimension, logical_state, theta)
    elif BC == 'matching':
        toric_ground_matchingBC(dimension)



def toric_code_mixedBC(A, B, dimension):
    if dimension == '3by3':
        qubits = 9
        coeffs = [-A, -A, -A, -A, -B, -B, -B, -B] # A for Vertex (Blue), B for Plaqutte (Purple)
        ops = [qml.PauliZ(1) @ qml.PauliZ(2) @ qml.PauliZ(4) @qml.PauliZ(5),
               qml.PauliZ(3) @ qml.PauliZ(4) @ qml.PauliZ(6) @qml.PauliZ(7),
               qml.PauliZ(0) @ qml.PauliZ(3),
               qml.PauliZ(5) @ qml.PauliZ(8),
               qml.PauliX(0) @ qml.PauliX(1) @ qml.PauliX(3) @qml.PauliX(4),
               qml.PauliX(4) @ qml.PauliX(5) @ qml.PauliX(7) @qml.PauliX(8),
               qml.PauliX(1) @ qml.PauliX(2),
               qml.PauliX(6) @ qml.PauliX(7)]
        H = qml.Hamiltonian(coeffs, ops)

    if dimension == '5by5':
        qubits = 25
        coeffs = [-A, -A, -A, -A, -A, -A, -A, -A, -A, -A, -A, -A,
                  -B, -B, -B, -B, -B, -B, -B, -B, -B, -B, -B, -B]
        ops = [qml.PauliZ(1) @ qml.PauliZ(2) @ qml.PauliZ(6) @qml.PauliZ(7),
               qml.PauliZ(3) @ qml.PauliZ(4) @ qml.PauliZ(8) @ qml.PauliZ(9),
               qml.PauliZ(5) @ qml.PauliZ(6) @ qml.PauliZ(10) @ qml.PauliZ(11),
               qml.PauliZ(7) @ qml.PauliZ(8) @ qml.PauliZ(12) @ qml.PauliZ(13),
               qml.PauliZ(11) @ qml.PauliZ(12) @ qml.PauliZ(16) @ qml.PauliZ(17),
               qml.PauliZ(13) @ qml.PauliZ(14) @ qml.PauliZ(18) @ qml.PauliZ(19),
               qml.PauliZ(15) @ qml.PauliZ(16) @ qml.PauliZ(20) @ qml.PauliZ(21),
               qml.PauliZ(17) @ qml.PauliZ(18) @ qml.PauliZ(22) @ qml.PauliZ(23),
               qml.PauliZ(0) @ qml.PauliZ(5),
               qml.PauliZ(10) @ qml.PauliZ(15),
               qml.PauliZ(9) @ qml.PauliZ(14),
               qml.PauliZ(19) @ qml.PauliZ(24),

               qml.PauliX(0) @ qml.PauliX(1) @ qml.PauliX(5) @ qml.PauliX(6),
               qml.PauliX(2) @ qml.PauliX(3) @ qml.PauliX(7) @ qml.PauliX(8),
               qml.PauliX(6) @ qml.PauliX(7) @ qml.PauliX(11) @ qml.PauliX(12),
               qml.PauliX(8) @ qml.PauliX(9) @ qml.PauliX(13) @ qml.PauliX(14),
               qml.PauliX(10) @ qml.PauliX(11) @ qml.PauliX(15) @ qml.PauliX(16),
               qml.PauliX(12) @ qml.PauliX(13) @ qml.PauliX(17) @ qml.PauliX(18),
               qml.PauliX(16) @ qml.PauliX(17) @ qml.PauliX(21) @ qml.PauliX(22),
               qml.PauliX(18) @ qml.PauliX(19) @ qml.PauliX(23) @ qml.PauliX(24),
               qml.PauliX(1) @ qml.PauliX(2),
               qml.PauliX(3) @ qml.PauliX(4),
               qml.PauliX(20) @ qml.PauliX(21),
               qml.PauliX(22) @ qml.PauliX(23)]
        H = qml.Hamiltonian(coeffs, ops)
    return qubits, H

def toric_code_matchingBC(A, B, dimension):

    if dimension == '12qubits':
        qubits = 12
        coeffs = [-A, -A, -A, -A, -A, -A, -A, -A, -A, -B, -B, -B, -B]
        ops = [qml.PauliZ(0) @ qml.PauliZ(2),
               qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(3),
               qml.PauliZ(1) @ qml.PauliZ(4),
               qml.PauliZ(2) @ qml.PauliZ(5) @ qml.PauliZ(7),
               qml.PauliZ(3) @ qml.PauliZ(5) @ qml.PauliZ(6) @ qml.PauliZ(8),
               qml.PauliZ(4) @ qml.PauliZ(6) @ qml.PauliZ(9),
               qml.PauliZ(7) @ qml.PauliZ(10),
               qml.PauliZ(8) @ qml.PauliZ(10) @ qml.PauliZ(11),
               qml.PauliZ(9) @ qml.PauliZ(11),

               qml.PauliX(0) @ qml.PauliX(2) @ qml.PauliX(3) @ qml.PauliX(5),
               qml.PauliX(1) @ qml.PauliX(3) @ qml.PauliX(4) @ qml.PauliX(6),
               qml.PauliX(5) @ qml.PauliX(7) @ qml.PauliX(8) @ qml.PauliX(10),
               qml.PauliX(6) @ qml.PauliX(8) @ qml.PauliX(9) @ qml.PauliX(11)]
        H = qml.Hamiltonian(coeffs, ops)
        return qubits, H


def toric_ground_mixedBC(dimension, logical_state, theta):

    if dimension == '3by3':
        if logical_state == '0' or logical_state == '1':
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

            if logical_state == '1':
                qml.PauliH(1)
                qml.PauliX(4)
                qml.PauliX(7)

        elif logical_state == 'plus':
            qml.Hadamard(0)
            qml.Hadamard(1)
            qml.Hadamard(6)
            qml.Hadamard(8)

            qml.CNOT(wires=[1, 2])
            qml.CNOT(wires=[6, 7])

            qml.CNOT(wires=[1, 4])
            qml.CNOT(wires=[6, 3])
            qml.CNOT(wires=[8, 5])

            qml.CNOT(wires=[0, 3])
            qml.CNOT(wires=[2, 5])
            qml.CNOT(wires=[7, 4])

            for i in range(9):
                qml.Hadamard(i)

        if logical_state == 'arbitrary':
            qml.Hadamard(0)
            qml.Hadamard(2)
            qml.Hadamard(5)
            qml.Hadamard(6)
            qml.RY(theta, wires=4)
            qml.CNOT(wires=[4, 1])
            qml.CNOT(wires=[4, 7])

            qml.CNOT(wires=[0, 3])
            qml.CNOT(wires=[5, 8])

            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[5, 4])
            qml.CNOT(wires=[6, 7])

            qml.CNOT(wires=[2, 1])
            qml.CNOT(wires=[3, 4])
            qml.CNOT(wires=[8, 7])

def toric_ground_matchingBC(dimension):

    if dimension == '12qubits':
        qml.Hadamard(0)
        qml.Hadamard(1)
        qml.Hadamard(5)
        qml.Hadamard(6)

        qml.CNOT(wires=[0, 2])
        qml.CNOT(wires=[1, 3])
        qml.CNOT(wires=[5, 7])
        qml.CNOT(wires=[6, 8])

        qml.CNOT(wires=[0, 3])
        qml.CNOT(wires=[1, 4])
        qml.CNOT(wires=[5, 8])
        qml.CNOT(wires=[6, 9])

        qml.CNOT(wires=[2, 5])
        qml.CNOT(wires=[4, 6])
        qml.CNOT(wires=[7, 10])
        qml.CNOT(wires=[9, 11])




