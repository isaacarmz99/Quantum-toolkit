"""Grover's search algorithm for a single marked state.

This is a minimal, from-scratch implementation (no qiskit_algorithms
dependency) so you can see exactly how the oracle and diffuser work,
rather than calling a black-box library function.
"""
from __future__ import annotations

import math

from qiskit import QuantumCircuit


def _oracle(num_qubits: int, marked_state: str) -> QuantumCircuit:
    """Flip the phase of the marked computational basis state.

    `marked_state` uses Qiskit's own bit ordering: the leftmost
    character is the highest-indexed qubit, matching how counts are
    displayed after a measurement.
    """
    qc = QuantumCircuit(num_qubits, name="oracle")
    zero_positions = [i for i, bit in enumerate(reversed(marked_state)) if bit == "0"]

    if zero_positions:
        qc.x(zero_positions)
    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)
    if zero_positions:
        qc.x(zero_positions)
    return qc


def _diffuser(num_qubits: int) -> QuantumCircuit:
    """Amplify the amplitude of the marked state (inversion about the mean)."""
    qc = QuantumCircuit(num_qubits, name="diffuser")
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))
    return qc


def grover_circuit(marked_state: str, iterations: int | None = None) -> QuantumCircuit:
    """Build a full Grover search circuit for a single marked bitstring.

    Args:
        marked_state: bitstring to search for, e.g. "11" or "101".
        iterations: number of Grover iterations. Defaults to the
            theoretically optimal count, floor(pi/4 * sqrt(2^n)).
    """
    num_qubits = len(marked_state)
    if iterations is None:
        iterations = max(1, math.floor((math.pi / 4) * math.sqrt(2 ** num_qubits)))

    qc = QuantumCircuit(num_qubits, num_qubits, name="grover")
    qc.h(range(num_qubits))

    oracle = _oracle(num_qubits, marked_state)
    diffuser = _diffuser(num_qubits)
    for _ in range(iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diffuser, inplace=True)

    qc.measure(range(num_qubits), range(num_qubits))
    return qc
