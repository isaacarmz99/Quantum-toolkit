"""QAOA (Quantum Approximate Optimization Algorithm) for Max-Cut.

Max-Cut is the canonical combinatorial optimization problem for QAOA:
partition graph nodes into two sets to maximize the number of edges
crossing between them. This is the same problem family as the
QUBO-based portfolio optimization from the project roadmap, just
easier to verify by hand.
"""
from __future__ import annotations

from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA


def maxcut_hamiltonian(num_nodes: int, edges: list[tuple[int, int]]) -> SparsePauliOp:
    """Build the Ising Hamiltonian whose minimum eigenvalue solves Max-Cut.

    For each edge (i, j), contributes 0.5 * (Z_i Z_j - I). Since
    Z_i Z_j = -1 when the edge is cut and +1 otherwise, minimizing the
    sum over all edges is equivalent to maximizing the number of cuts.
    """
    pauli_list = []
    for i, j in edges:
        z_string = ["I"] * num_nodes
        z_string[i] = "Z"
        z_string[j] = "Z"
        pauli_list.append(("".join(z_string), 0.5))

    identity_term = "I" * num_nodes
    pauli_list.append((identity_term, -0.5 * len(edges)))
    return SparsePauliOp.from_list(pauli_list)


def run_qaoa(num_nodes: int, edges: list[tuple[int, int]], reps: int = 2):
    """Run QAOA on a Max-Cut problem.

    Returns:
        (result, hamiltonian) — result.eigenvalue is negative the best
        cut value found; -result.eigenvalue.real gives the cut size.
    """
    hamiltonian = maxcut_hamiltonian(num_nodes, edges)
    sampler = StatevectorSampler()
    optimizer = COBYLA(maxiter=200)

    qaoa = QAOA(sampler, optimizer, reps=reps)
    result = qaoa.compute_minimum_eigenvalue(hamiltonian)
    return result, hamiltonian
