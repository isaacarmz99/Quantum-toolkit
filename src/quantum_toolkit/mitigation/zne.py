"""Zero-noise extrapolation (ZNE) via unitary folding.

The core idea: you can't dial noise down on real hardware, so instead
you deliberately dial it UP by a known amount, measure an observable
at several noise levels, and extrapolate the trend back to what it
would be at zero noise.

The "dialing up" is done via unitary folding: replacing a circuit U
with U (U-dagger U)^n. Ideally U-dagger U is the identity, so the
computed result doesn't change - but the physical circuit is now
longer, so it accumulates roughly proportionally more real noise.
"""
from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit, transpile


def fold_circuit(circuit: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """Stretch a circuit's noise without changing its ideal output.

    `circuit` must not contain measurements - fold the state-preparation
    part only, and measure separately afterward.

    Args:
        scale_factor: how much to scale the noise by. Must be a
            positive odd integer (1 = no folding, 3 = one fold, ...).
    """
    if scale_factor < 1 or scale_factor % 2 == 0:
        raise ValueError("scale_factor must be a positive odd integer (1, 3, 5, ...)")
    if circuit.num_clbits:
        raise ValueError("fold_circuit expects a circuit with no measurements")

    n_folds = (scale_factor - 1) // 2
    folded = circuit.copy()
    inverse = circuit.inverse()
    for _ in range(n_folds):
        folded.compose(inverse, inplace=True)
        folded.compose(circuit, inplace=True)
    return folded


def extrapolate_to_zero(scale_factors: list, probabilities: list) -> dict:
    """Fit a line through (scale, probability) points and extrapolate to scale=0.

    Pulled out as its own pure function (no simulator, no randomness) so
    the extrapolation math itself can be tested deterministically,
    separately from the statistical noise of live quantum sampling.
    """
    coeffs = np.polyfit(scale_factors, probabilities, deg=1)
    zero_noise_estimate = float(np.clip(np.polyval(coeffs, 0), 0.0, 1.0))
    return {
        "fit_coefficients": coeffs.tolist(),
        "zero_noise_estimate": zero_noise_estimate,
    }


def zero_noise_extrapolate(
    state_prep_circuit: QuantumCircuit,
    backend,
    target_bitstring: str,
    scale_factors: list = (1, 3, 5),
    shots: int = 4096,
    seed: int | None = None,
) -> dict:
    """Estimate P(target_bitstring) at each noise scale, then extrapolate to zero.

    Returns a dict with the raw (scale -> probability) measurements, the
    linear fit coefficients, and the extrapolated zero-noise estimate.
    """
    probabilities = []

    for scale in scale_factors:
        folded = fold_circuit(state_prep_circuit, scale)
        folded.measure_all()
        transpiled = transpile(folded, backend=backend, optimization_level=1)
        counts = backend.run(transpiled, shots=shots, seed_simulator=seed).result().get_counts()
        prob = counts.get(target_bitstring, 0) / shots
        probabilities.append(prob)

    fit = extrapolate_to_zero(list(scale_factors), probabilities)

    return {
        "scale_factors": list(scale_factors),
        "probabilities": probabilities,
        **fit,
    }