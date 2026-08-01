import pytest
from qiskit import transpile
from qiskit_aer import AerSimulator

from quantum_toolkit.circuits.basics import bell_state_circuit, ghz_state_circuit


def test_bell_state_only_produces_00_and_11():
    qc = bell_state_circuit()
    backend = AerSimulator()
    result = backend.run(transpile(qc, backend), shots=1000).result()
    counts = result.get_counts()

    # A correct Bell state never collapses to 01 or 10.
    assert set(counts.keys()) <= {"00", "11"}
    assert counts.get("00", 0) > 0
    assert counts.get("11", 0) > 0


def test_bell_state_outcomes_are_roughly_balanced():
    qc = bell_state_circuit()
    backend = AerSimulator()
    result = backend.run(transpile(qc, backend), shots=4000).result()
    counts = result.get_counts()

    # With enough shots, 00 and 11 should each land near 50%.
    # Loose tolerance since this is a statistical test, not exact.
    ratio = counts.get("00", 0) / sum(counts.values())
    assert 0.4 < ratio < 0.6


def test_ghz_state_only_produces_all_zero_or_all_one():
    n = 4
    qc = ghz_state_circuit(n)
    backend = AerSimulator()
    result = backend.run(transpile(qc, backend), shots=1000).result()
    counts = result.get_counts()

    valid_states = {"0" * n, "1" * n}
    assert set(counts.keys()) <= valid_states


def test_ghz_rejects_fewer_than_two_qubits():
    with pytest.raises(ValueError):
        ghz_state_circuit(1)
