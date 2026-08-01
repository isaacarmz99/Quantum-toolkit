"""Circuit benchmarking framework.

Runs a circuit (or set of circuits) across one or more backends and
collects structural and runtime metrics: depth, gate counts,
execution time, and (optionally) output fidelity against a reference
distribution. This is the kind of internal tooling real quantum
software teams build and maintain.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


@dataclass
class BenchmarkResult:
    circuit_name: str
    backend_name: str
    depth: int
    gate_counts: dict
    execution_time_s: float
    counts: dict | None = None
    fidelity: float | None = None


def _hellinger_fidelity(counts_a: dict, counts_b: dict) -> float:
    """Hellinger fidelity between two measurement count distributions.

    Returns a value in [0, 1], where 1 means identical distributions.
    """
    shots_a = sum(counts_a.values())
    shots_b = sum(counts_b.values())
    keys = set(counts_a) | set(counts_b)
    bhattacharyya_coeff = sum(
        ((counts_a.get(k, 0) / shots_a) * (counts_b.get(k, 0) / shots_b)) ** 0.5
        for k in keys
    )
    return bhattacharyya_coeff ** 2


class QuantumBenchmark:
    """Benchmarks circuits across one or more backends.

    Defaults to a local AerSimulator. Pass real backends (e.g. from
    qiskit-ibm-runtime) to extend this to actual hardware — see
    Phase 8 in the project roadmap.
    """

    def __init__(self, backends: list | None = None, shots: int = 2048):
        self.backends = backends or [AerSimulator()]
        self.shots = shots

    def run(
        self,
        circuit: QuantumCircuit,
        reference_counts: dict | None = None,
    ) -> list[BenchmarkResult]:
        results = []
        for backend in self.backends:
            transpiled = transpile(circuit, backend=backend, optimization_level=1)

            start = time.perf_counter()
            job = backend.run(transpiled, shots=self.shots)
            counts = job.result().get_counts()
            elapsed = time.perf_counter() - start

            fidelity = None
            if reference_counts is not None:
                fidelity = _hellinger_fidelity(counts, reference_counts)

            backend_name = getattr(backend, "name", backend.__class__.__name__)
            if callable(backend_name):
                backend_name = backend_name()

            results.append(
                BenchmarkResult(
                    circuit_name=circuit.name,
                    backend_name=backend_name,
                    depth=transpiled.depth(),
                    gate_counts=dict(transpiled.count_ops()),
                    execution_time_s=elapsed,
                    counts=counts,
                    fidelity=fidelity,
                )
            )
        return results

    def run_many(self, circuits: list[QuantumCircuit]) -> dict[str, list[BenchmarkResult]]:
        return {circuit.name: self.run(circuit) for circuit in circuits}
