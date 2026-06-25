# Reproduced facts — substrate-floor paper (captured run outputs)

Regenerate: see code/README.md. All commands are seeded/deterministic and read-only on committed artifacts.

Date captured: 2026-06-24 (R&R revision: 3-prior MC + bootstrap CIs)

## 1. Monte-Carlo verdict regions + divergence fractions, 3 priors + 95% bootstrap CIs (paper §Monte-Carlo Verdict Regions, §Companion Computation Script)
```
$ uv run --with numpy python code/verdict_regions_mc.py
# Verdict-region Monte Carlo (seed 20260624, n = 200,000, 95% bootstrap CIs over 1000 resamples)

## prior = uniform
  verdict regions:  corroborated=.120  contested=.230  substrate-conditional=.250  jointly-unresolved=.400
  4a non-pooling   (vs random-effects pool)   .880 [.878, .881]
  4b no-rescue     (vs Dempster-Shafer fusion) .214 [.212, .216]
  4c typed-verdict (vs conformal/selective)    .480 [.477, .482]

## prior = beta25
  verdict regions:  corroborated=.032  contested=.095  substrate-conditional=.256  jointly-unresolved=.617
  4a non-pooling   (vs random-effects pool)   .968 [.967, .969]
  4b no-rescue     (vs Dempster-Shafer fusion) .178 [.176, .180]
  4c typed-verdict (vs conformal/selective)    .351 [.349, .353]

## prior = truncnorm
  verdict regions:  corroborated=.132  contested=.186  substrate-conditional=.156  jointly-unresolved=.526
  4a non-pooling   (vs random-effects pool)   .868 [.866, .869]
  4b no-rescue     (vs Dempster-Shafer fusion) .395 [.393, .397]
  4c typed-verdict (vs conformal/selective)    .342 [.340, .344]

```

## 2. Reconciliation lattice — four typed verdicts on committed cases (paper §Worked Demonstrations)
```
$ uv run --with pyyaml python code/substrate_floor.py --all
[ext_fit_corroborated_with_closematch] C-experiential-fit -> CORROBORATED
    covering=['SBT', 'ExternalEquityLens']  resolvers=['SBT', 'ExternalEquityLens']  abstain=[]
    dispersion=0.02  max_self_floor=0.03  effective_floor=0.03  consensus=0.11  S/N=3.67
    within_floor=True  verdict_entropy=0.0
    ALIGNMENT RISK (non-exact, possible false agreement): ['ExternalEquityLens(closeMatch,external)']
    why: resolvers agree within their floors (dispersion 0.02 <= 0.03) and the consensus clears the effective floor (S/N 3.67 >= 2.0)
[ma_fit_corroborated] C-experiential-fit -> CORROBORATED
    covering=['SBT', 'OST']  resolvers=['SBT', 'OST']  abstain=[]
    dispersion=0.02  max_self_floor=0.03  effective_floor=0.03  consensus=0.1  S/N=3.33
    within_floor=True  verdict_entropy=0.0
    why: resolvers agree within their floors (dispersion 0.02 <= 0.03) and the consensus clears the effective floor (S/N 3.33 >= 2.0)
[ma_fit_contested] C-experiential-fit -> CONTESTED
    covering=['SBT', 'OST']  resolvers=['SBT', 'OST']  abstain=[]
    dispersion=0.55  max_self_floor=0.05  effective_floor=0.55  consensus=0.475  S/N=0.86
    within_floor=False  verdict_entropy=0.0
    why: resolvers disagree beyond their floors (dispersion 0.55 > max self-floor 0.05) — characterize why; human judgment required
[ma_fit_substrate_conditional] C-experiential-fit -> SUBSTRATE-CONDITIONAL
    covering=['SBT', 'OST']  resolvers=['SBT']  abstain=['OST']
    dispersion=0.0  max_self_floor=0.05  effective_floor=0.05  consensus=0.4  S/N=8.0
    within_floor=True  verdict_entropy=1.0
    why: one substrate resolves (S/N 8.0 >= 2.0); the rest abstain — the finding holds only under that apparatus
[ma_fit_jointly_unresolved] C-experiential-fit -> JOINTLY-UNRESOLVED
    covering=['SBT', 'OST']  resolvers=[]  abstain=['SBT', 'OST']
    dispersion=0.0  max_self_floor=None  effective_floor=0.0  consensus=None  S/N=None
    within_floor=False  verdict_entropy=0.0
    why: every covering substrate abstains
[ma_fit_agreement_on_noise] C-experiential-fit -> JOINTLY-UNRESOLVED
    covering=['SBT', 'OST']  resolvers=['SBT', 'OST']  abstain=[]
    excluded (audit fail, §1): ['UNVETTED-3P']
    dispersion=0.01  max_self_floor=0.05  effective_floor=0.05  consensus=0.025  S/N=0.5
    within_floor=True  verdict_entropy=0.0
    ALIGNMENT RISK (non-exact, possible false agreement): ['OST(closeMatch,declared)']
    why: resolvers agree but the consensus is below floor (S/N 0.5 < 2.0) — agreement on noise, honestly unknown
[ma_fit_unaligned_false_agreement] C-experiential-fit -> CONTESTED
    covering=['SBT', 'OST']  resolvers=['SBT', 'OST']  abstain=[]
    dispersion=0.02  max_self_floor=0.03  effective_floor=0.03  consensus=0.1  S/N=3.33
    within_floor=True  verdict_entropy=0.0
    ALIGNMENT RISK (non-exact, possible false agreement): ['SBT(unaligned,computed)', 'OST(unaligned,computed)']
    why: resolvers agree numerically, but their anchor terms are UNALIGNED in the graph (SBT, OST) — possible false agreement across distinct concepts; human judgment required before corroborating

[substrate-floor] 7 reconciliation(s); PASS
```

## 3. Live measurement floor — SBT operator floor read from committed atlas (paper §One Rule, Two Instrument Kinds)
```
$ uv run --with pyyaml python code/verify_contract.py --all

=== EXAMPLE_case.yaml ===
  [WARN] q1: resolved verdict has no resolution block — not machine-verifiable
  (no resolution blocks — use verify_case.py for the structural check)
  -> PASS  [0 resolution(s) checked]

=== EXAMPLE_contract_case.yaml ===
  [OK] q1: resolved: magnitude 0.0469 clears the live operator floor 0.0232
  [OK] q2: abstained: magnitude 0.0012 below the live operator floor 0.0232
  -> PASS  [2 resolution(s) checked]

=== EXAMPLE_full_floor_case.yaml ===
  (no resolution blocks — use verify_case.py for the structural check)
  -> PASS  [0 resolution(s) checked]

=== EXAMPLE_live_case.yaml ===
  (no resolution blocks — use verify_case.py for the structural check)
  -> PASS  [0 resolution(s) checked]

=== example_harbor_full_reuse.yaml ===
  [OK] q1: resolved: magnitude 0.0812 clears the live operator floor 0.0103
  -> PASS  [1 resolution(s) checked]

=== example_lumen_reuse.yaml ===
  [OK] q1: resolved: magnitude 0.0574 clears the live operator floor 0.0068
  -> PASS  [1 resolution(s) checked]

=== ferrari_luce_reuse.yaml ===
  [OK] q1: abstained: magnitude 0.1119 below the live artifact floor 0.1171
  [OK] q2: abstained: magnitude 0.0413 below the live artifact floor 0.1171
  -> PASS  [2 resolution(s) checked]

========================================================
7/7 case(s) honest; 0 with drift
```

## 4. Live coherence floor — OST specification instrument (paper §One Rule, Two Instrument Kinds)
```
$ uv run --with pyyaml python code/verify_ost_contract.py --all

=== EXAMPLE_meridian_transfer.yaml ===
  [OK] q1: resolved: magnitude 0.2100 clears the live combined coherence floor 0.0833
  [OK] q2: abstained: magnitude 0.0500 below the live combined coherence floor 0.0833
  -> PASS  [2 resolution(s) checked]

========================================================
1/1 case(s) honest; 0 with drift
```

## 5. Public-benchmark reconciliation — substrate floor on real cross-KIND data (paper §A public-benchmark reconciliation)
```
$ uv run --with pyyaml python code/public_benchmark_reconciliation.py
# Public-benchmark reconciliation (substrate floor on real cross-KIND data)
# snapshot: Llama 3.1 release comparison table (Dubey et al. 2024); accessed 2026-06-25
# instrument floors are binomial SEs from documented N; axis floor Phi(1)-0.5 = 0.341

Per-benchmark accuracy floor (binomial SE at ~85% accuracy, by test-set size N):
  MMLU       N= 14042  floor ~= 0.30 pp   (broad-knowledge multiple-choice)
  MATH       N=  5000  floor ~= 0.50 pp   (competition mathematics (free-response))
  HumanEval  N=   164  floor ~= 2.79 pp   (code synthesis (pass@1, execution-tested))

## claim: GPT-4o outperforms Claude-3.5-Sonnet  via ['MMLU', 'MATH']
   MMLU       margin  +0.40pp  floor 0.38pp  z=+1.05  value=0.853  -> resolve
   MATH       margin  +5.50pp  floor 0.88pp  z=+6.27  value=1.000  -> resolve
   => VERDICT: CORROBORATED
      resolvers agree within their floors (dispersion 0.1467 <= 0.3413) and the consensus clears the effective floor (S/N 2.71 >= 2.0)

## claim: GPT-4o outperforms Llama-3.1-405B  via ['MMLU', 'HumanEval']
   MMLU       margin  +0.10pp  floor 0.38pp  z=+0.26  value=0.604  -> abstain
   HumanEval  margin  +1.20pp  floor 3.37pp  z=+0.36  value=0.639  -> abstain
   => VERDICT: JOINTLY-UNRESOLVED
      every covering substrate abstains

## claim: Llama-3.1-405B outperforms Claude-3.5-Sonnet  via ['MATH', 'HumanEval']
   MATH       margin  +2.70pp  floor 0.89pp  z=+3.02  value=0.999  -> resolve
   HumanEval  margin  -3.00pp  floor 3.23pp  z=-0.93  value=0.177  -> abstain
   => VERDICT: SUBSTRATE-CONDITIONAL
      one substrate resolves (S/N 2.93 >= 2.0); the rest abstain — the finding holds only under that apparatus

## claim: GPT-4o outperforms Claude-3.5-Sonnet  via ['MATH', 'HumanEval']
   MATH       margin  +5.50pp  floor 0.88pp  z=+6.27  value=1.000  -> resolve
   HumanEval  margin  -1.80pp  floor 3.14pp  z=-0.57  value=0.283  -> abstain
   => VERDICT: SUBSTRATE-CONDITIONAL
      one substrate resolves (S/N 2.93 >= 2.0); the rest abstain — the finding holds only under that apparatus

[public-benchmark] 4 reconciliation(s) computed from the committed snapshot.
```
