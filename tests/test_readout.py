from quantum_toolkit.mitigation.noise_models import noisy_backend
from quantum_toolkit.mitigation.readout import build_calibration_matrix, mitigate_counts


def test_calibration_matrix_diagonal_dominates_for_low_noise():
    backend = noisy_backend(
        readout_error_prob=0.02, depolarizing_prob_1q=0.0, depolarizing_prob_2q=0.0
    )
    matrix = build_calibration_matrix(backend, num_qubits=1, shots=4096)

    assert matrix[0][0] > 0.9
    assert matrix[1][1] > 0.9


def test_mitigate_counts_shifts_toward_true_distribution():
    backend = noisy_backend(
        readout_error_prob=0.1, depolarizing_prob_1q=0.0, depolarizing_prob_2q=0.0
    )
    calibration = build_calibration_matrix(backend, num_qubits=1, shots=8192)

    raw_counts = {"0": 500, "1": 4500}
    corrected = mitigate_counts(raw_counts, calibration, num_qubits=1)

    total = sum(corrected.values())
    frac_one = corrected.get("1", 0) / total
    assert frac_one > 0.9