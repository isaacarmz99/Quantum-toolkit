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