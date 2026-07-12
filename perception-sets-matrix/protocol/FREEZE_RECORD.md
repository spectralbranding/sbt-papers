# FREEZE_RECORD — 2026bf pre-registered campaign (Perception Sets the Matrix)

**Frozen**: 2026-07-12, before any campaign API call fired.
**Unit suite**: 9/9 passed before freeze (planted-positive, null, and
weighted-planted controls included).
**Amendment discipline**: the frozen layers below are never edited after this
record; changes go to the append-only `amendments:` section of PROTOCOL.yaml
and are reported in the paper.

Pre-freeze correction (recorded per protocol): the canonical five corpus
brand profiles were removed from the design after verification that they are
illustrative (2026d Table 5 notes + stated limitation), not empirical
measurements — they cannot serve as recovery ground truth. Floor F1 is
computed from the campaign's own repeated readings; floor F3 from the
authored Study-1 pack targets (ground truth by construction).

## SHA-256 checksums of the frozen layer set

| Layer | File | SHA-256 |
|---|---|---|
| Pre-registration | PREREG_STUDY_DESIGN.md (internal frozen original; public copy at protocol/PREREG_STUDY_DESIGN.md carries two documented administrative redactions) | 7a2d39ef669d49a7a3e3dffe3e64b023bd1e03fde3c005f169ee8bdf70524dac |
| Protocol config | PROTOCOL.yaml | 732c2904ff014a09026ffe97ffa223479bebdc29c97b2f936caf0df10e0b5572 |
| Study-1 stimuli | STIMULI_STUDY1.yaml | ddb37ea60b4cf53efd3b9b44515fc6ada44466da42ddd31405d5cdd92ea4d26c |
| Study-2 brand sets | BRANDS_STUDY2.yaml | 8baffcce24213f1622df2910ed85a8be7129f0476bd937b729848557124344a0 |
| Cohort personas | PERSONAS.yaml | c05f6df5bc7a64ea854c150fc08c139b655afba435171ba28801af517258ecc1 |
| Prompt set + providers | code/psm_lib.py | b09aed8433b5c8f4f05e5904ebd7e33bcd7a7e757736bea6a8344b5f3a876639 |
| Collection harness | code/run_campaign.py | f1846c25f3091dd22993183ab2c8c558ed39b51e4f3e0f27d73dcf69721e8c8a |
| Frozen estimator | code/estimator.py | 98254fd5a8d7ffac7baa98e7a28d1811496fdc46e5bc5e9273510bf02c47ef59 |
| Design generator | code/gen_design.py | 81d9196cd3cfb36af9a725d9c06d09cf5ecf8ecf971f442a77371932ff5193e2 |
| Unit suite | code/tests/test_psm_estimator.py | b1b69190294bcf05145746a5230d87633c13ccc7767c3d17ae9c3c080f6abf23 |

## Frozen decisions (summary)

- Operators: OP1 claude-sonnet-5, OP2 claude-haiku-4-5-20251001 (Anthropic);
  OP3 gpt-5.5-2026-04-23, OP4 gpt-5.4-mini-2026-03-17 (OpenAI); OP5
  deepseek-v4-pro, OP6 deepseek-v4-flash (DeepSeek). Reserves: qwen3.7-max-
  2026-06-08, qwen3.6-flash-2026-04-16 (Alibaba); replacement only on hard
  API unavailability.
- Study 2 categories/brands: QSR coffee (Starbucks, Dunkin', Tim Hortons,
  Peet's Coffee, Blue Bottle Coffee); athletic footwear (Nike, Adidas,
  New Balance, Hoka, Asics).
- Arms: validate (OP1+OP3 x 6 packs x r3, gate MAD <= 1.5 BEFORE the
  propensity arm); cohort validation r1; brand readings r3; eliciting r3;
  same-call r1.
- Analysis: PROTOCOL.yaml `analysis:` block (tau_b, within-cohort permutation
  10,000 draws, pooled median, alpha .05, tau floor .20, positive direction;
  delta_tau; delta_tau_w paired swap permutation; induced matrix moment
  matching; band = middle tercile of fitted link; frozen robustness list;
  K1-K4).
- Seed everywhere: 20260712.

## Amendment A1 (2026-07-12, pre-campaign)

Deepseek thinking-tier token-cap fix in the harness (see PROTOCOL.yaml
amendments). Zero campaign calls had fired. Updated checksums:
code/run_campaign.py = 984ac4c943251bcba1868067a9a1d78654e08a16a684793315588ff47ba0bd31; PROTOCOL.yaml = 3f6e6d385ecd8a0f0ddb7e7e68d48e4444fd2e7e8bde503c0839b66eda2d9ea2.

## Amendment A2 (2026-07-12, during collection)

Formatting-only reformat (black + flake8 E231 whitespace) of the code layer —
zero semantic change; unit suite re-run green (9/9) post-format. Updated
checksums:
code/psm_lib.py = 6e90e7e652043f8d1ac0955d2196ba916d857c70a4cffd76f06031aead5f8326
code/run_campaign.py = 9fcc6bc78ada8440b5cc838e7b9a108b3fab8e0a0d67b78dd18eb5e542be7ff6
code/estimator.py = 725bbe19961b47d476b2c81ce7e265c74f1a575ab1597419270ea50d36fa0bc0
code/gen_design.py = f752cf950a34deafb46045db5646e6dfb4ac83c17893af8cacfffd4a72a38d42
code/tests/test_psm_estimator.py = b81088b1265d5c778569a81d401a6dd1f062f2cc3a848dbff4ccc6635162a7b6

## Amendment A3 (2026-07-12, during collection)

Anthropic thinking-tier token-cap fix (same class as A1; see PROTOCOL.yaml
amendments). Updated checksums: code/run_campaign.py = 2f3b40f963004db8559e4f420f62ff679da48d4d7137af8a02d25d08e4710423;
PROTOCOL.yaml = 1313efc96f6a873407b5fc89049c206da1727df33d44327ba6803612d4c7a416.
