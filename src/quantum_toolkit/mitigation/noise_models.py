"""Synthetic noise models for testing and demonstrating error mitigation.

Real hardware noise isn't something you control or choose — these
exist purely to give the mitigation techniques something to correct
for when running locally, since Qiskit's simulator is noiseless by
default.
"""
from __future__ import annotations

from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error


def noisy_backend(
    depolarizing_prob_1q: float = 0.01,
    depolarizing_prob_2q: float = 0.05,
    readout_error_prob: float = 0.04,
) -> AerSimulator:
    """Build an AerSimulator with depolarizing gate noise and readout noise.

    Defaults are deliberately exaggerated compared to real hardware so
    the effect of mitigation is clearly visible over a few thousand shots.
    """
    noise_model = NoiseModel()

    error_1q = depolarizing_error(depolarizing_prob_1q, 1)
    error_2q = depolarizing_error(depolarizing_prob_2q, 2)
    noise_model.add_all_qubit_quantum_error(
        error_1q, ["h", "x", "sx", "rz", "u1", "u2", "u3"]
    )
    noise_model.add_all_qubit_quantum_error(error_2q, ["cx"])

    readout_error = ReadoutError(
        [
            [1 - readout_error_prob, readout_error_prob],
            [readout_error_prob, 1 - readout_error_prob],
        ]
    )
    noise_model.add_all_qubit_readout_error(readout_error)

    return AerSimulator(noise_model=noise_model)