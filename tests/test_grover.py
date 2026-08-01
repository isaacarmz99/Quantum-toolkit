from qiskit import transpile
from qiskit_aer import AerSimulator

from quantum_toolkit.circuits.grover import grover_circuit


def test_grover_finds_marked_state_with_high_probability():
    marked = "11"
    qc = grover_circuit(marked)
    backend = AerSimulator()
    result = backend.run(transpile(qc, backend), shots=2000).result()
    counts = result.get_counts()

    top_result = max(counts, key=counts.get)
    assert top_result == marked
    # Grover's should concentrate most probability on the marked state.
    assert counts[marked] / sum(counts.values()) > 0.7


def test_grover_finds_marked_state_for_three_qubits():
    marked = "101"
    qc = grover_circuit(marked)
    backend = AerSimulator()
    result = backend.run(transpile(qc, backend), shots=2000).result()
    counts = result.get_counts()

    top_result = max(counts, key=counts.get)
    assert top_result == marked
