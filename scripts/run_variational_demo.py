"""Run VQE and QAOA and print results.

These are iterative optimizations and take longer than the basic
circuits, so they're kept separate from run_demo.py.

Run with:
    python scripts/run_variational_demo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from quantum_toolkit.circuits.qaoa import run_qaoa
from quantum_toolkit.circuits.vqe import example_hamiltonian, run_vqe


def main():
    print("Running VQE on a 2-qubit Hamiltonian...")
    hamiltonian = example_hamiltonian()
    vqe_result = run_vqe(hamiltonian)
    print(f"  Estimated ground state energy: {vqe_result.eigenvalue.real:.4f}")

    print("\nRunning QAOA on a 4-node Max-Cut problem...")
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    qaoa_result, _ = run_qaoa(num_nodes=4, edges=edges)
    print(f"  Best cut value found: {-qaoa_result.eigenvalue.real:.4f}")
    print(f"  (out of {len(edges)} total edges)")


if __name__ == "__main__":
    main()
