# Companion computation

Every computed value the paper reports, re-derivable from published sources. Two scripts re-read the
frozen probe records; two are pure simulation and read nothing.

## Reproducing

The records are not in this repository — they are the dataset of record, published separately at
[spectralbranding/entity-name-leakage](https://huggingface.co/datasets/spectralbranding/entity-name-leakage)
(DOI [10.57967/hf/10159](https://doi.org/10.57967/hf/10159)). Download it and hand the orchestrator
the collection directory:

```
hf download spectralbranding/entity-name-leakage --repo-type dataset --local-dir enl-data
./reproduce.sh enl-data/second_collection
```

`reproduce.sh` runs the four scripts below in order. To run one on its own:

```
uv run code/estimate_guard_ratio.py  --data-root enl-data/second_collection
uv run code/per_dimension_leakage.py --data-root enl-data/second_collection
uv run code/equivalence_power.py
uv run code/simulate_guard_power.py
```

`uv` is the only prerequisite: each script pins its own dependencies inline (PEP 723), so nothing
needs installing and the versions are the ones the reported values were produced under. Seeds are
fixed (`SEED = 20260829`). All four were run twice and produce byte-identical tables in
`output/tables/`.

The collection directory is the one holding `data/` and `PROTOCOL.yaml`. Passing `--data-root` every
time gets old; `$ENL_DATA_ROOT` sets it once.

## What each script answers

| Script | Question | Answer | Paper |
|---|---|---|---|
| `estimate_guard_ratio.py` | How large is the text-by-entity interaction against the **within-cell residual**? | **.066 and .039 across two runs, mean .053** | Table 4 |
| `per_dimension_leakage.py` | Does the leakage concentrate on particular dimensions, or spread across them? | Largest and smallest differ by a factor of 2.4, both extremes reproducing across runs | Table 3 |
| `equivalence_power.py` | How many texts are needed to **demonstrate** neutrality rather than fail to reject it? | 95% upper bound: **.159 at 4 texts, .108 at 16, .100 at 24, .086 at 48** | Table 5 |
| `simulate_guard_power.py` | How many texts make the neutrality guard's verdict reproducible across two runs? | At the measured ratio the guard behaves like the null; **stability is not the binding constraint** | Discussion |

## Two things worth knowing before trusting any of it

**The estimator carries a validation that can fail, and it did.** Before reporting a ratio,
`estimate_guard_ratio.py` recomputes the probe's own published aggregate name effect and requires a
match to within .01. The first implementation used mean|Δ| across dimensions and returned .580
against a published .824 — **the validation failed and stopped the run.** The probe's per-dimension
metric is Euclidean distance ÷ √8 (RMS), defined in the collection's own `code/stats_core.py`. With
the correct metric the pipeline reproduces .824 and .825 exactly. A validation that could not fail
would have let a 30%-low number through.

**The F-quantile approximation validates itself.** `simulate_guard_power.py` uses a Wilson-Hilferty
approximation rather than `scipy`. Its ratio-0 column *is* the false-positive rate, and it lands on
.05 across eight different `(df1, df2)` pairs. If the approximation were wrong that column would
drift off nominal, so the table checks its own machinery.

## Scope

`SD_residual` and the class means are taken from the measured probe data. `S_TEXT` is a stated
assumption, not a measurement. The interaction ratio fed to `equivalence_power.py` is the measured
value, so its bounds describe *this* instrument and domain — nine names, cookware artifacts — and
not dimensional rating tasks in general.

**These scripts do not set the neutrality bound.** They supply sampling behaviour. The bound must be
grounded rather than invented, and stated relative to the value it takes when the effect is absent.
