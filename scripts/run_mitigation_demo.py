"""Compare raw (noisy), ZNE-corrected, and readout-corrected results.

Run with:
    python scripts/run_mitigation_demo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from qiskit import transpile

from quantum_toolkit.circuits.basics import bell_state_circuit
from quantum_toolkit.mitigation.noise_models import noisy_backend
from quantum_toolkit.mitigation.readout import build_calibration_matrix, mitigate_counts
from quantum_toolkit.mitigation.zne import zero_noise_extrapolate


def main():
    backend = noisy_backend(depolarizing_prob_2q=0.06, readout_error_prob=0.04)
    qc_no_measure = bell_state_circuit(measure=False)
    qc_with_measure = bell_state_circuit(measure=True)

    print("Bell state P(11) — ideal value is 0.500\n")

    transpiled = transpile(qc_with_measure, backend=backend, optimization_level=1)
    raw_counts = backend.run(transpiled, shots=4096).result().get_counts()
    raw_prob = raw_counts.get("11", 0) / sum(raw_counts.values())
    print(f"  Raw (noisy):          {raw_prob:.3f}")

    zne_result = zero_noise_extrapolate(
        qc_no_measure, backend, target_bitstring="11", scale_factors=[1, 3, 5], shots=4096
    )
    print(f"  ZNE-corrected:        {zne_result['zero_noise_estimate']:.3f}")

    calibration = build_calibration_matrix(backend, num_qubits=2, shots=4096)
    mitigated_counts = mitigate_counts(raw_counts, calibration, num_qubits=2)
    mitigated_prob = mitigated_counts.get("11", 0) / sum(mitigated_counts.values())
    print(f"  Readout-corrected:    {mitigated_prob:.3f}")


if __name__ == "__main__":
    main()