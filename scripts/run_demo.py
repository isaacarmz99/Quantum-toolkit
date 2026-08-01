"""Quick demo: build each circuit, benchmark it, and print a summary table.

Run with:
    python scripts/run_demo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from quantum_toolkit.benchmarking.benchmark import QuantumBenchmark
from quantum_toolkit.circuits.basics import bell_state_circuit, ghz_state_circuit
from quantum_toolkit.circuits.grover import grover_circuit


def main():
    circuits = [
        bell_state_circuit(),
        ghz_state_circuit(4),
        grover_circuit("11"),
    ]

    bench = QuantumBenchmark(shots=2048)

    print(f"{'Circuit':<15}{'Backend':<18}{'Depth':<8}{'Time (s)':<10}{'Top result'}")
    print("-" * 65)
    for circuit in circuits:
        for result in bench.run(circuit):
            top_result = max(result.counts, key=result.counts.get)
            print(
                f"{result.circuit_name:<15}{result.backend_name:<18}"
                f"{result.depth:<8}{result.execution_time_s:<10.4f}{top_result}"
            )


if __name__ == "__main__":
    main()
