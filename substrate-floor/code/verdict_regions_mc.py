#!/usr/bin/env python3
"""Monte-Carlo verdict-region characterization for the reconciliation lattice (paper ME1/RC3).

Companion computation script for "The Substrate Floor: Nested Noise Floors for Auditable
Abstention Across Heterogeneous Instruments." Reproduces the verdict-region fractions and the
three prior-art divergence fractions reported in the paper's Methods/Results (P4, lemmas
4a/4b/4c; RC3). Self-contained: replicates the two-instrument [0,1] lattice of the reference
implementation (code/substrate_floor.py) on the smallest sufficient model (M1) and
sweeps it by Monte Carlo.

Model (M1). Two instruments on a normalized verdict axis in [0,1]. Each instrument i emits a
verdict value v_i and exposes its own combined noise floor f_i. It RESOLVES iff its own signal
clears its own floor, v_i > k_marginal * f_i, else it ABSTAINS. The substrate dispersion is
D = |v_1 - v_2|; the effective (nested) floor is effective_floor = max(D, f_1, f_2) over the
resolving instruments; the consensus is the mean of the resolvers' values; S/N = consensus /
effective_floor. The typed verdict follows the lattice exactly as substrate_floor.py computes it.

Divergence fractions (the empirical content of P4):
  4a NON-POOLING vs random-effects meta-analysis: a random-effects pool always emits a pooled
     point estimate; the lattice declines one whenever it returns contested / substrate-
     conditional / jointly-unresolved. Reported as the fraction of cases where the lattice
     withholds the pooled mean the prior method would assert.
  4b NO-RESCUE vs Dempster-Shafer / sensor fusion: fusion combines two agreeing sources into a
     confident value even when both are individually below floor; the lattice returns
     jointly-unresolved (agreement on noise). Reported as the fraction of "agreement-on-noise"
     cases (both resolve, agree within floors, but consensus below the effective floor).
  4c TYPED-VERDICT vs conformal / selective prediction: a binary abstain-or-predict rule cannot
     represent a typed verdict. Reported as the fraction of cases carrying a typed verdict
     (contested or substrate-conditional) that a binary rule collapses to a single predict/abstain.

Robustness (Grok post-draft ask). The verdict values are drawn under three priors — uniform
(uninformative headline), beta(2,5) (claims skewed weak), truncated-normal (mean .5, sd .2) — and
each divergence fraction carries a 95% nonparametric bootstrap CI (1000 resamples). The divergence
ORDER is prior-robust (4a stays high, 4b and 4c remain substantial); the exact fractions are
prior-dependent, which is reported honestly rather than tuned away.

Reproduce:
    uv run --with numpy python code/verdict_regions_mc.py
    uv run --with numpy python code/verdict_regions_mc.py --prior uniform
Fixed seed 20260624; 200,000 draws per prior. Prints a markdown-ready summary to stdout.
"""

from __future__ import annotations

import argparse

import numpy as np

SEED = 20260624
N_DRAWS = 200_000
PLACES = 4

CORROBORATED = "corroborated"
CONTESTED = "contested"
SUBSTRATE_CONDITIONAL = "substrate-conditional"
JOINTLY_UNRESOLVED = "jointly-unresolved"
VERDICTS = (CORROBORATED, CONTESTED, SUBSTRATE_CONDITIONAL, JOINTLY_UNRESOLVED)


def classify(
    v1: float,
    v2: float,
    f1: float,
    f2: float,
    k_resolve: float = 2.0,
    k_marginal: float = 1.0,
) -> tuple[str, bool]:
    """Replicate the substrate_floor.py lattice on the two-instrument [0,1] model (M1).

    Returns (verdict, agreement_on_noise). agreement_on_noise marks the no-rescue region used
    for the Lemma-4b divergence fraction: both resolve, agree within floors, consensus below the
    effective floor.
    """
    res_vals: list[float] = []
    res_floors: list[float] = []
    for v, f in ((v1, f1), (v2, f2)):
        if (
            v > k_marginal * f
        ):  # the instrument's own signal clears its own floor -> resolve
            res_vals.append(v)
            res_floors.append(f)

    n = len(res_vals)
    if n == 0:
        return JOINTLY_UNRESOLVED, False

    if n == 1:
        eff = max(res_floors[0], 0.0)
        sn = abs(res_vals[0]) / eff if eff > 0 else None
        if sn is not None and sn >= k_resolve:
            return SUBSTRATE_CONDITIONAL, False
        return JOINTLY_UNRESOLVED, False

    dispersion = abs(res_vals[0] - res_vals[1])
    max_self_floor = max(res_floors)
    effective_floor = max(dispersion, max_self_floor)
    consensus = sum(res_vals) / n
    sn = abs(consensus) / effective_floor if effective_floor > 0 else None
    within_floor = dispersion <= max_self_floor

    if not within_floor:
        return CONTESTED, False
    if sn is not None and sn >= k_resolve:
        return CORROBORATED, False
    # both resolve, agree within floors, but the consensus does not clear the effective floor:
    # the agreement-on-noise region the no-rescue lemma forbids fusion from rescuing.
    return JOINTLY_UNRESOLVED, True


# Verdict integer codes for the vectorized classifier (order matches VERDICTS).
_CODE = {v: i for i, v in enumerate(VERDICTS)}


def _sample_values(rng: np.random.Generator, n: int, prior: str) -> np.ndarray:
    """Draw verdict values in [0,1] under one of three priors (Grok robustness ask).

    uniform        — deliberately uninformative (the headline characterization).
    beta(2,5)      — claims skewed weak (most real signals are small).
    truncnorm      — values concentrated near .5 (mean .5, sd .2), rejection-sampled to [0,1].
    """
    if prior == "uniform":
        return rng.uniform(0.0, 1.0, n)
    if prior == "beta25":
        return rng.beta(2.0, 5.0, n)
    if prior == "truncnorm":
        out = np.empty(n)
        filled = 0
        while filled < n:
            cand = rng.normal(0.5, 0.2, n)
            cand = cand[(cand >= 0.0) & (cand <= 1.0)]
            take = min(len(cand), n - filled)
            out[filled : filled + take] = cand[:take]
            filled += take
        return out
    raise ValueError(f"unknown prior: {prior}")


def classify_vec(
    v1: np.ndarray,
    v2: np.ndarray,
    f1: np.ndarray,
    f2: np.ndarray,
    k_resolve: float = 2.0,
    k_marginal: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized form of classify(): returns (verdict_codes, on_noise_mask).

    Bit-for-bit equivalent to the scalar classifier, which mirrors substrate_floor.py.
    """
    n = v1.shape[0]
    code = np.full(n, _CODE[JOINTLY_UNRESOLVED], dtype=np.int8)
    on_noise = np.zeros(n, dtype=bool)

    r1 = v1 > k_marginal * f1
    r2 = v2 > k_marginal * f2
    n_res = r1.astype(np.int8) + r2.astype(np.int8)

    # exactly one resolves -> substrate-conditional iff it clears k_resolve, else jointly-unresolved
    one = n_res == 1
    v_one = np.where(r1, v1, v2)
    f_one = np.where(r1, f1, f2)
    sn_one = np.where(f_one > 0, np.abs(v_one) / np.maximum(f_one, 1e-12), 0.0)
    code[one & (sn_one >= k_resolve)] = _CODE[SUBSTRATE_CONDITIONAL]

    # both resolve
    two = n_res == 2
    disp = np.abs(v1 - v2)
    max_floor = np.maximum(f1, f2)
    eff = np.maximum(disp, max_floor)
    consensus = (v1 + v2) / 2.0
    sn_two = np.where(eff > 0, np.abs(consensus) / np.maximum(eff, 1e-12), 0.0)
    within = disp <= max_floor
    contested = two & (~within)
    corro = two & within & (sn_two >= k_resolve)
    noise = two & within & (sn_two < k_resolve)  # agreement on noise (no-rescue region)
    code[contested] = _CODE[CONTESTED]
    code[corro] = _CODE[CORROBORATED]
    code[noise] = _CODE[JOINTLY_UNRESOLVED]
    on_noise[noise] = True
    return code, on_noise


def _bootstrap_ci(
    indicator: np.ndarray, rng: np.random.Generator, b: int = 1000
) -> tuple[float, float]:
    """Nonparametric 95% bootstrap CI on the mean of a 0/1 indicator over draws."""
    n = indicator.shape[0]
    means = np.empty(b)
    for j in range(b):
        idx = rng.integers(0, n, n)
        means[j] = indicator[idx].mean()
    lo, hi = np.percentile(means, [2.5, 97.5])
    return float(lo), float(hi)


def run(n_draws: int = N_DRAWS, seed: int = SEED, prior: str = "uniform") -> dict:
    rng = np.random.default_rng(seed)
    v1 = _sample_values(rng, n_draws, prior)
    v2 = _sample_values(rng, n_draws, prior)
    # Floors uniform on (0, 0.5] throughout, so the prior isolates the effect of the verdict-value
    # distribution (the quantity the lattice keys on) on the verdict regions.
    f1 = rng.uniform(1e-6, 0.5, n_draws)
    f2 = rng.uniform(1e-6, 0.5, n_draws)

    code, on_noise = classify_vec(v1, v2, f1, f2)
    region = {k: float((code == _CODE[k]).mean()) for k in VERDICTS}

    nonpool = (code != _CODE[CORROBORATED]).astype(np.int8)
    typed = (
        (code == _CODE[CONTESTED]) | (code == _CODE[SUBSTRATE_CONDITIONAL])
    ).astype(np.int8)
    no_rescue = on_noise.astype(np.int8)

    boot = np.random.default_rng(seed + 1)
    div = {
        "4a_nonpooling": (float(nonpool.mean()), *_bootstrap_ci(nonpool, boot)),
        "4b_no_rescue": (float(no_rescue.mean()), *_bootstrap_ci(no_rescue, boot)),
        "4c_typed_verdict": (float(typed.mean()), *_bootstrap_ci(typed, boot)),
    }
    return {
        "n": n_draws,
        "seed": seed,
        "prior": prior,
        "region_fractions": region,
        "divergence": div,
    }


def _fmt(x: float) -> str:
    """No leading zero for values below 1 (paper standard)."""
    s = f"{x:.3f}"
    return s[1:] if s.startswith("0.") else s


def _fmt_ci(triple: tuple) -> str:
    p, lo, hi = triple
    return f"{_fmt(p)} [{_fmt(lo)}, {_fmt(hi)}]"


PRIORS = ("uniform", "beta25", "truncnorm")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=N_DRAWS, help="Monte-Carlo draws")
    ap.add_argument("--seed", type=int, default=SEED, help="RNG seed")
    ap.add_argument(
        "--prior", choices=PRIORS + ("all",), default="all", help="value prior"
    )
    args = ap.parse_args()

    priors = PRIORS if args.prior == "all" else (args.prior,)
    print(
        f"# Verdict-region Monte Carlo (seed {args.seed}, n = {args.n:,}, "
        f"95% bootstrap CIs over 1000 resamples)\n"
    )
    for prior in priors:
        r = run(args.n, args.seed, prior)
        rf = r["region_fractions"]
        dv = r["divergence"]
        print(f"## prior = {prior}")
        print(
            "  verdict regions:  " + "  ".join(f"{k}={_fmt(rf[k])}" for k in VERDICTS)
        )
        print(
            f"  4a non-pooling   (vs random-effects pool)   {_fmt_ci(dv['4a_nonpooling'])}"
        )
        print(
            f"  4b no-rescue     (vs Dempster-Shafer fusion) {_fmt_ci(dv['4b_no_rescue'])}"
        )
        print(
            f"  4c typed-verdict (vs conformal/selective)    {_fmt_ci(dv['4c_typed_verdict'])}"
        )
        print()


if __name__ == "__main__":
    main()
