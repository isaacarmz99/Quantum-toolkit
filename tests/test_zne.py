import pytest

from quantum_toolkit.circuits.basics import bell_state_circuit
from quantum_toolkit.mitigation.noise_models import noisy_backend
from quantum_toolkit.mitigation.zne import (
    extrapolate_to_zero,
    fold_circuit,
    zero_noise_extrapolate,
)


def _bell_state_without_measurement():
    return bell_state_circuit(measure=False)


def test_fold_circuit_rejects_even_scale_factor():
    qc = _bell_state_without_measurement()
    with pytest.raises(ValueError):
        fold_circuit(qc, 2)


def test_fold_circuit_rejects_circuit_with_measurements():
    qc = bell_state_circuit(measure=True)
    with pytest.raises(ValueError):
        fold_circuit(qc, 3)


def test_fold_circuit_preserves_qubit_count():
    qc = _bell_state_without_measurement()
    folded = fold_circuit(qc, 3)
    assert folded.num_qubits == qc.num_qubits


def test_fold_circuit_scale_one_is_unchanged_depth():
    qc = _bell_state_without_measurement()
    folded = fold_circuit(qc, 1)
    assert folded.depth() == qc.depth()


def test_extrapolate_to_zero_recovers_linear_trend_exactly():
    # Synthetic, noise-free data: probability drops by exactly 0.05 per
    # unit of scale factor. No simulator involved, so this is fully
    # deterministic - it tests the extrapolation math itself, not
    # statistical sampling, which is what kept making this test flaky.
    scale_factors = [1, 3, 5]
    probabilities = [0.45, 0.35, 0.25]
    fit = extrapolate_to_zero(scale_factors, probabilities)

    assert fit["zero_noise_estimate"] == pytest.approx(0.5, abs=1e-6)


def test_zero_noise_extrapolation_runs_against_a_noisy_backend():
    # Smoke test against a live, statistically noisy simulator: checks
    # the full pipeline runs end-to-end and produces a sane result.
    # Deliberately NOT asserting an exact statistical comparison here -
    # that's the deterministic test above's job.
    qc = _bell_state_without_measurement()
    backend = noisy_backend(depolarizing_prob_2q=0.12, readout_error_prob=0.05)

    result = zero_noise_extrapolate(
        qc, backend, target_bitstring="11", scale_factors=[1, 3, 5], shots=8192, seed=42
    )

    assert 0.0 <= result["zero_noise_estimate"] <= 1.0
    assert len(result["probabilities"]) == 3