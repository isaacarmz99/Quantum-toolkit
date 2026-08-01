# Quantum Software Engineering Toolkit

[![Tests](https://github.com/isaacarmz99/Quantum-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/isaacarmz99/Quantum-toolkit/actions)

A hands-on portfolio project for breaking into quantum computing roles.
Implements canonical quantum algorithms, benchmarks them across
backends, and applies error mitigation techniques — all with real test
coverage, which most beginner quantum projects skip entirely.

## Status: Phases 1–4 complete, 18 passing tests

- **Phase 1 — Quantum SDK fluency**: Bell state, GHZ state (`circuits/basics.py`)
- **Phase 2 — Algorithm breadth**: Grover's search, VQE, QAOA (`circuits/`)
- **Phase 3 — Benchmarking framework**: runs circuits across backends,
  reports depth, gate counts, execution time, and fidelity (`benchmarking/benchmark.py`)
- **Phase 4 — Error mitigation**: zero-noise extrapolation via unitary
  folding, and readout error correction via calibration matrix
  inversion (`mitigation/`)

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
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

Compare raw vs. mitigated results on a synthetic noisy backend:

```bash
python scripts/run_mitigation_demo.py
```

Run the test suite:

```bash
pytest -v
```

## Project structure
src/quantum_toolkit/
circuits/
basics.py # Bell state, GHZ state
grover.py # Grover's search (from-scratch oracle + diffuser)
vqe.py # Variational Quantum Eigensolver
qaoa.py # QAOA for Max-Cut
benchmarking/
benchmark.py # QuantumBenchmark: runs circuits, collects metrics
mitigation/
noise_models.py # synthetic noise for testing/demos
zne.py # zero-noise extrapolation via unitary folding
readout.py # readout error mitigation via calibration matrix
tests/ # pytest suite for everything above (18 tests)
scripts/ # runnable demos
.github/workflows/ # CI: runs pytest automatically on every push

## Notable bugs found along the way

Kept here deliberately as part of the project's history, not scrubbed out:

- **Grover oracle crash on all-ones marked states** - calling a gate on
  an empty qubit list broke when the marked bitstring was all 1s (e.g.
  `"11"`). Caught by the test suite, not by eyeballing the code.
- **Grover iteration count overshoot** - the iteration formula used
  `round()` instead of `floor()`, which overshoots the optimal
  measurement probability for small qubit counts and can swing back
  toward baseline odds. Also caught by tests, not inspection.
- **Flaky statistical test in ZNE** - an early test asserted an exact
  statistical comparison against live, randomly-sampled simulator
  output, which is inherently fragile at reasonable shot counts. Fixed
  by separating the deterministic extrapolation math (unit-testable
  with synthetic data) from a loose end-to-end smoke test against the
  real noisy backend.

## Roadmap

- [x] Phase 1: Quantum SDK fluency
- [x] Phase 2: Algorithm breadth (Grover, VQE, QAOA)
- [x] Phase 3: Benchmarking framework
- [x] Phase 4: Error mitigation (zero-noise extrapolation, readout correction)
- [x] Phase 5: Test suite (18 tests and growing)
- [x] Phase 6: Public repo with CI wired up
- [ ] Phase 7: Contribute a PR to Qiskit, PennyLane, or Cirq
- [ ] Phase 8: Benchmark across IBM Quantum + Amazon Braket hardware

## Notes on API versions

This targets Qiskit 1.x+, using the `qiskit_algorithms` package and
primitives-based patterns (`StatevectorEstimator`, `StatevectorSampler`).
Qiskit's API has shifted significantly across major versions - if an
import fails, check your installed version with `pip show qiskit`
against the current Qiskit docs; the fix is usually a renamed import
path, not a logic error.