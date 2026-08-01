"""Foundational quantum circuits: Bell state and GHZ state.

These are the "hello world" circuits of quantum computing, used to
demonstrate superposition and entanglement.
"""
from qiskit import QuantumCircuit


def bell_state_circuit(measure: bool = True) -> QuantumCircuit:
    """Build a 2-qubit Bell state (maximally entangled) circuit.

    Produces the state (|00> + |11>) / sqrt(2).
    """
    qc = QuantumCircuit(2, 2 if measure else 0, name="bell_state")
    qc.h(0)
    qc.cx(0, 1)
    if measure:
        qc.measure([0, 1], [0, 1])
    return qc


def ghz_state_circuit(num_qubits: int = 3, measure: bool = True) -> QuantumCircuit:
    """Build an n-qubit GHZ state circuit.

    Produces the state (|00...0> + |11...1>) / sqrt(2), generalizing
    the Bell state to more qubits.
    """
    if num_qubits < 2:
        raise ValueError("GHZ state requires at least 2 qubits")

    qc = QuantumCircuit(num_qubits, num_qubits if measure else 0, name="ghz_state")
    qc.h(0)
    for target in range(1, num_qubits):
        qc.cx(0, target)
    if measure:
        qc.measure(range(num_qubits), range(num_qubits))
    return qc
