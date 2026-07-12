# Web Appendix — Perception Sets the Matrix (2026bf)

All values in this appendix are read verbatim from the frozen estimator output (`data/results.json`, seed 20260712, 10,000-draw permutation nulls) and the supplementary metameric check (`data/metameric_check.json`, protocol amendment A4). Regenerate with `uv run python code/gen_web_appendix.py`.

## Table A1: Per-Operator Floor Panel.

| Operator | Model | F1 ICC(2,1) | F2 sum-check rate | F2 Juster tau | F3 recovery MAD | F4 failure rate | Passes all |
|---|---|---|---|---|---|---|---|
| OP1 | claude-sonnet-5 | .990 | .900 | .843 | 0.736 | .077 | no |
| OP2 | claude-haiku-4-5-20251001 | .933 | 1.000 | .853 | 1.163 | .000 | yes |
| OP3 | gpt-5.5-2026-04-23 | .994 | 1.000 | .850 | 1.021 | .000 | yes |
| OP4 | gpt-5.4-mini-2026-03-17 | .967 | 1.000 | .788 | 1.156 | .000 | yes |
| OP5 | deepseek-v4-pro | .931 | 1.000 | .894 | 1.188 | .005 | yes |
| OP6 | deepseek-v4-flash | .919 | 1.000 | .914 | 0.899 | .000 | yes |

*Notes*: Frozen floors — F1 reading test-retest ICC(2,1) >= .60; F2 constant-sum check rate >= .95 and Juster-vs-constant-sum rank agreement tau >= .5; F3 known-profile recovery mean absolute deviation <= 1.5 scale points per dimension (authored Study-1 targets); F4 refusal/malformed-output rate <= .05. OP1 was demoted on F2 and F4 per the frozen demotion rule and excluded from the primary pool (reported in the paper).

## Table A2: Induced-Matrix Detail by Category.

### Specialty coffee (synthetic, Study 1)

Concentration S = 11.788; induced diagonal vs observed repeat ordering tau = .867.

| Brand | Share s | Closed-form diagonal | Observed repeat |
|---|---|---|---|
| Ember & Oak Roasters | .218 | .279 | .305 |
| Voltbean | .237 | .297 | .248 |
| Common Ground Collective | .243 | .302 | .327 |
| DailyDrip | .075 | .148 | .199 |
| Maison Noir Café | .042 | .117 | .122 |
| Fairmile Coffee | .184 | .248 | .209 |

### Quick-service coffee (Study 2)

Concentration S = 21.161; induced diagonal vs observed repeat ordering tau = .000.

| Brand | Share s | Closed-form diagonal | Observed repeat |
|---|---|---|---|
| Starbucks | .270 | .303 | .348 |
| Dunkin' | .214 | .249 | .365 |
| Tim Hortons | .122 | .162 | .277 |
| Peet's Coffee | .193 | .229 | .386 |
| Blue Bottle Coffee | .201 | .237 | .357 |

### Athletic footwear (Study 2)

Concentration S = 29.598; induced diagonal vs observed repeat ordering tau = .400.

| Brand | Share s | Closed-form diagonal | Observed repeat |
|---|---|---|---|
| Nike | .236 | .261 | .287 |
| Adidas | .209 | .235 | .296 |
| New Balance | .230 | .255 | .360 |
| Hoka | .150 | .178 | .259 |
| Asics | .175 | .202 | .240 |

*Notes*: Share vector s from mean propensity shares; S by moment-matching the across-cohort propensity dispersion to the Dirichlet variance relation; diagonal from the closed form P = (I + S 1 s^T) / (S + 1). Observed repeat propensities from the descriptive switching probes (illustrative arm).

## Table A3: Intermediate-Band Mass and Cohort-Profile Dispersion.

| Category | Band mass | Cohort-profile dispersion |
|---|---|---|
| Specialty coffee (synthetic, Study 1) | .477 | 10.653 |
| Quick-service coffee (Study 2) | .408 | 10.662 |
| Athletic footwear (Study 2) | .040 | 10.813 |

*Notes*: The space-filling cohort design fixed dispersion nearly constant across categories, so the pre-registered dispersion-tracking secondary had no leverage this campaign (band mass tracked link strength instead); the dispersion prediction awaits a design that varies dispersion deliberately.

## Table A4: Operator-Level Metameric Pairs (Amendment A4).

| Category | Operator | Pair | Profile distance | Reading floor | Median propensity diff | Elicitation floor | Within floor |
|---|---|---|---|---|---|---|---|
| coffee_roasters | OP2 | Ember & Oak Roasters - Voltbean | 6.557 | 7.018 | .200 | .029 | no |
| coffee_roasters | OP2 | Voltbean - Common Ground Collective | 5.766 | 7.018 | .200 | .029 | no |
| coffee_roasters | OP2 | Voltbean - Maison Noir Café | 6.305 | 7.018 | .200 | .029 | no |
| coffee_roasters | OP2 | Voltbean - Fairmile Coffee | 4.000 | 7.018 | .100 | .029 | no |
| athletic_footwear | OP5 | Nike - Adidas | 1.414 | 2.179 | .100 | .035 | no |
| athletic_footwear | OP6 | Nike - Adidas | 2.693 | 2.915 | .100 | .068 | no |

*Notes*: A pair is metameric for an operator when the distance between the operator's median brand profiles falls below that operator's own reading floor. In all six pairs the median cohort propensity difference exceeds the elicitation floor — the metameric-equality prediction (P4) is violated where exercisable.
