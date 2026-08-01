"""Variational Quantum Eigensolver (VQE) for a simple Hamiltonian.

VQE is a hybrid quantum-classical algorithm: a parameterized quantum
circuit prepares a trial state, and a classical optimizer tunes the
parameters to minimize the expectation value of a target Hamiltonian
(its lowest eigenvalue approximates the ground state energy).

Uses qiskit_algorithms and the primitives API, matching the patterns
used in most production quantum software today.
"""
from __future__ import annotations

from qiskit.circuit.library import EfficientSU2
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA


def example_hamiltonian() -> SparsePauliOp:
    """A small 2-qubit Hamiltonian with a known minimum eigenvalue.

    H = Z0 Z1 + 0.5 * X0 + 0.5 * X1
    """
    return SparsePauliOp.from_list([
        ("ZZ", 1.0),
        ("XI", 0.5),
        ("IX", 0.5),
    ])


def run_vqe(hamiltonian: SparsePauliOp | None = None):
    """Run VQE and return the qiskit_algorithms VQEResult."""
    hamiltonian = hamiltonian if hamiltonian is not None else example_hamiltonian()
    ansatz = EfficientSU2(hamiltonian.num_qubits, reps=1)
    estimator = StatevectorEstimator()
    optimizer = COBYLA(maxiter=200)

    vqe = VQE(estimator, ansatz, optimizer)
    result = vqe.compute_minimum_eigenvalue(hamiltonian)
    return result
