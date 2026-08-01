from quantum_toolkit.benchmarking.benchmark import QuantumBenchmark
from quantum_toolkit.circuits.basics import bell_state_circuit


def test_benchmark_returns_expected_metrics():
    qc = bell_state_circuit()
    bench = QuantumBenchmark(shots=500)
    results = bench.run(qc)

    assert len(results) == 1
    result = results[0]
    assert result.circuit_name == "bell_state"
    assert result.depth > 0
    assert result.execution_time_s > 0
    assert sum(result.counts.values()) == 500


def test_benchmark_computes_fidelity_against_reference():
    qc = bell_state_circuit()
    bench = QuantumBenchmark(shots=1000)
    reference = {"00": 500, "11": 500}
    result = bench.run(qc, reference_counts=reference)[0]

    assert result.fidelity is not None
    assert 0.0 <= result.fidelity <= 1.0


def test_benchmark_fidelity_is_high_for_identical_distributions():
    qc = bell_state_circuit()
    bench = QuantumBenchmark(shots=2000)
    result = bench.run(qc)[0]
    # Compare the run against itself: fidelity should be ~1.0.
    fidelity = bench.run(qc, reference_counts=result.counts)[0].fidelity

    assert fidelity > 0.9


def test_run_many_covers_every_circuit():
    circuits = [bell_state_circuit(), bell_state_circuit()]
    circuits[1].name = "bell_state_2"
    bench = QuantumBenchmark(shots=200)

    results = bench.run_many(circuits)

    assert set(results.keys()) == {"bell_state", "bell_state_2"}
