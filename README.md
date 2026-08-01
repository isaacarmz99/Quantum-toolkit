[Tests](https://github.com/isaacarmz99/quantum-toolkit/actions/workflows/tests.yml/badge.svg)


# Quantum Software Engineering Toolkit

A hands-on portfolio project for breaking into quantum computing roles.
Implements canonical quantum algorithms, benchmarks them across
backends, and (eventually) adds error mitigation — all with real test
coverage, which most beginner quantum projects skip entirely.

## Status: Phases 1–3 scaffolded

- **Phase 1 — Quantum SDK fluency**: Bell state, GHZ state (`circuits/basics.py`)
- **Phase 2 — Algorithm breadth**: Grover's search, VQE, QAOA (`circuits/`)
- **Phase 3 — Benchmarking framework**: runs circuits across backends,
  reports depth, gate counts, execution time, and fidelity (`benchmarking/benchmark.py`)

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

Run the basic circuits and Grover's search through the benchmarking framework:

```bash
python scripts/run_demo.py
```

Run VQE and QAOA (slower — iterative optimization):

```bash
python scripts/run_variational_demo.py
```

Run the test suite:

```bash
pytest -v
```

## Project structure

```
src/quantum_toolkit/
  circuits/
    basics.py     # Bell state, GHZ state
    grover.py     # Grover's search (from-scratch oracle + diffuser)
    vqe.py        # Variational Quantum Eigensolver
    qaoa.py       # QAOA for Max-Cut
  benchmarking/
    benchmark.py  # QuantumBenchmark: runs circuits, collects metrics
tests/            # pytest suite for everything above
scripts/          # runnable demos
.github/workflows/  # CI skeleton (runs pytest on push)
```

## Roadmap

- [x] Phase 1: Quantum SDK fluency
- [x] Phase 2: Algorithm breadth (Grover, VQE, QAOA)
- [x] Phase 3: Benchmarking framework
- [ ] Phase 4: Error mitigation (zero-noise extrapolation, readout correction)
- [x] Phase 5: Test suite (started — expand as new modules are added)
- [ ] Phase 6: Publish as a proper package, wire up CI badge, polish docs
- [ ] Phase 7: Contribute a PR to Qiskit, PennyLane, or Cirq
- [ ] Phase 8: Benchmark across IBM Quantum + Amazon Braket hardware

## Notes on API versions

This targets Qiskit 1.x+, using the `qiskit_algorithms` package and
primitives-based patterns (`StatevectorEstimator`, `StatevectorSampler`).
Qiskit's API has shifted significantly across major versions — if an
import fails, check your installed version with `pip show qiskit`
against the current Qiskit docs; the fix is usually a renamed import
path, not a logic error.
