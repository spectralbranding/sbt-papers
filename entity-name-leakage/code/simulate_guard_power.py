# /// script
# requires-python = "==3.12.*"
# dependencies = ["numpy==2.4.3"]
# ///
"""Phase-2 power simulation: how many texts make the neutrality guard reproducible?

NOT study code. This is the pre-registration computation the gate and the thesis
both require BEFORE N_text is frozen, and it makes no model calls. It answers one
question:

    The follow-up probe's neutrality guard fired in run 2 and not in run 1, on
    four texts. A guard that flips between identical runs cannot license reading
    past it (K3). How many texts are needed before two independent runs AGREE?

The guard is the one manipulation-check rule 2 Route B prescribes: a text-by-entity
INTERACTION tested against the WITHIN-CELL RESIDUAL -- never against the entity main
effect, whose ratio moves with the main effect and with replicate count while the
interaction is fixed.

Model, per reading-pair magnitude y in cell (text t, class c), replicate i:

    y[t,c,i] = mu + T[t] + C[c] + TC[t,c] + e[t,c,i]

with T ~ N(0, s_T^2), C fixed (4 classes), TC ~ N(0, s_TC^2), e ~ N(0, s_e^2).

Cell counts follow the collected design: 9 names give C(9,2)=36 pairs per text,
distributed across the four classes in the proportions the follow-up actually
returned (II 60, RR_matched 121, RR_unmatched 179, RI 358 per run over 4 texts).

Run:
    uv run python code/simulate_guard_power.py

Seed is fixed. Output is deterministic.
"""

import numpy as np

SEED = 20260829
N_SIM = 4000
N_TEXTS = [4, 6, 8, 12, 16, 20, 24, 32]
# interaction SD as a multiple of within-cell residual SD; 0 is the true null
RATIOS = [0.0, 0.15, 0.30, 0.50]
ALPHA = 0.05

# per-text cell counts, from the follow-up probe's own class n's divided by 4 texts
CELL_N = {"II": 15, "RR_matched": 30, "RR_unmatched": 45, "RI": 90}
CLASSES = list(CELL_N)
# class means in test-retest units, from the probe -- shape only, NOT a claim
CLASS_MEAN = np.array([0.95, 1.16, 1.14, 1.13])
S_TEXT = (
    0.35  # text main-effect SD; the probe's TEXT share was the largest single component
)
S_RESID = 1.00  # within-cell residual SD; everything is expressed relative to this


def guard_verdict(rng, n_text, ratio):
    """One experiment. Returns True if the guard FIRES (texts judged non-neutral)."""
    n_c = np.array([CELL_N[c] for c in CLASSES])
    t_eff = rng.normal(0.0, S_TEXT, size=n_text)
    tc = rng.normal(0.0, ratio * S_RESID, size=(n_text, len(CLASSES)))

    cell_sum = np.zeros((n_text, len(CLASSES)))
    ss_within = 0.0
    for j, n in enumerate(n_c):
        mu = CLASS_MEAN[j] + t_eff[:, None] + tc[:, j][:, None]
        y = rng.normal(mu, S_RESID, size=(n_text, n))
        cell_sum[:, j] = y.sum(axis=1)
        ss_within += ((y - y.mean(axis=1, keepdims=True)) ** 2).sum()

    cell_mean = cell_sum / n_c[None, :]
    n_tot = n_text * n_c.sum()
    df_resid = n_tot - n_text * len(CLASSES)
    ms_resid = ss_within / df_resid

    # weighted two-way decomposition on the cell means
    w = np.broadcast_to(n_c[None, :], cell_mean.shape)
    grand = (cell_mean * w).sum() / w.sum()
    row = (cell_mean * w).sum(axis=1) / w.sum(axis=1)
    col = (cell_mean * w).sum(axis=0) / w.sum(axis=0)
    resid_cells = cell_mean - row[:, None] - col[None, :] + grand
    ss_inter = (w * resid_cells**2).sum()
    df_inter = (n_text - 1) * (len(CLASSES) - 1)
    ms_inter = ss_inter / df_inter

    f = ms_inter / ms_resid
    # upper-tail F critical value without scipy: Wilson-Hilferty approximation
    crit = f_crit(df_inter, df_resid, ALPHA)
    return f > crit


def f_crit(d1, d2, alpha):
    """Wilson-Hilferty approximation to the upper-alpha F quantile.

    Validated by the simulation itself: the ratio-0 column of the fire-rate table
    is the false-positive rate, and it lands on alpha across eight different
    (df1, df2) pairs. That check can fail, and would if this were wrong.
    """
    z = 1.6448536269514722 if abs(alpha - 0.05) < 1e-9 else _z(1 - alpha)
    a, b = 2.0 / (9.0 * d1), 2.0 / (9.0 * d2)
    t1, t2 = 1 - a, 1 - b
    disc = z * z * (a * t2**2 + b * t1**2) - a * b * z**4
    val = (t2 * t1 + np.sqrt(max(disc, 0.0))) / (t2**2 - b * z * z)
    if val <= 0:
        raise ValueError(f"F quantile approximation failed for df=({d1}, {d2})")
    return float(val**3)


def _z(p):
    # Acklam-style inverse normal, adequate at these tolerances
    from math import log, sqrt

    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    q = p - 0.5
    r = q * q
    return (
        (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
        * q
        / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    )


def main():
    rng = np.random.default_rng(SEED)
    print(
        f"Guard reproducibility across TWO independent runs (K3), {N_SIM} simulated pairs\n"
    )
    print(
        "interaction/residual ratio 0 = texts truly neutral; the guard SHOULD not fire\n"
    )
    header = "n_texts | " + " | ".join(f"ratio {r:.2f}" for r in RATIOS)
    print(header)
    print("-" * len(header))
    table = {}
    for n_text in N_TEXTS:
        cells = []
        for ratio in RATIOS:
            agree = 0
            fire1 = 0
            for _ in range(N_SIM):
                a = guard_verdict(rng, n_text, ratio)
                b = guard_verdict(rng, n_text, ratio)
                agree += int(a == b)
                fire1 += int(a)
            table[(n_text, ratio)] = (agree / N_SIM, fire1 / N_SIM)
            cells.append(f"  {agree / N_SIM:.3f}   ")
        print(f"{n_text:7d} | " + " | ".join(cells))

    print("\nFire rate in a single run (ratio .00 is the false-positive rate):\n")
    print(header)
    print("-" * len(header))
    for n_text in N_TEXTS:
        cells = [f"  {table[(n_text, r)][1]:.3f}   " for r in RATIOS]
        print(f"{n_text:7d} | " + " | ".join(cells))

    print("\nReading:")
    print("  A guard is USABLE when two independent runs agree. Agreement below ~.95")
    print("  means the verdict is a coin-flip and cannot license reading past it --")
    print("  which is exactly what happened on 4 texts.")


if __name__ == "__main__":
    main()
