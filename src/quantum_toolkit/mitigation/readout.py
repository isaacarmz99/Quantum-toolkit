"""Readout error mitigation via calibration matrix inversion.

Measurement itself is noisy: a qubit truly in |0> can be misreported
as |1>, and vice versa. We characterize this by preparing every basis
state and measuring it, building a "confusion matrix" of true state
vs. measured state, then use its (pseudo-)inverse to correct raw
counts from real experiments.
"""
from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit, transpile


def build_calibration_matrix(backend, num_qubits: int, shots: int = 4096) -> np.ndarray:
    """Build a 2^n x 2^n calibration matrix by measuring every basis state.

    matrix[i][j] = P(measured state i | prepared state j)
    """
    dim = 2**num_qubits
    matrix = np.zeros((dim, dim))

    for prepared in range(dim):
        qc = QuantumCircuit(num_qubits, num_qubits)
        bitstring = format(prepared, f"0{num_qubits}b")
        for qubit, bit in enumerate(reversed(bitstring)):
            if bit == "1":
                qc.x(qubit)
        qc.measure(range(num_qubits), range(num_qubits))

        transpiled = transpile(qc, backend=backend, optimization_level=0)
        counts = backend.run(transpiled, shots=shots).result().get_counts()

        for measured_bitstring, count in counts.items():
            measured = int(measured_bitstring, 2)
            matrix[measured][prepared] = count / shots

    return matrix


def mitigate_counts(raw_counts: dict, calibration_matrix: np.ndarray, num_qubits: int) -> dict:
    """Correct raw counts using the pseudo-inverse of the calibration matrix."""
    dim = 2**num_qubits
    raw_vector = np.zeros(dim)
    for bitstring, count in raw_counts.items():
        raw_vector[int(bitstring, 2)] = count

    corrected_vector = np.linalg.pinv(calibration_matrix) @ raw_vector

    corrected_vector = np.clip(corrected_vector, 0, None)
    total_raw = raw_vector.sum()
    total_corrected = corrected_vector.sum()
    if total_corrected > 0:
        corrected_vector *= total_raw / total_corrected

    corrected_counts = {}
    for state in range(dim):
        if corrected_vector[state] > 0.5:
            bitstring = format(state, f"0{num_qubits}b")
            corrected_counts[bitstring] = corrected_vector[state]
    return corrected_counts