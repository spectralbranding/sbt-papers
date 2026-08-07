# prism_core — shared PRISM campaign machinery

Shared module for PRISM-family empirical campaigns (PRISM-C 2026bb, PRISM-T
2026ba, and later members). Extracted 2026-07-02 from the frozen 2026az
(PRISM-M) campaign code — that campaign's `code/` directory is the published
companion of a completed run and is deliberately NOT modified;
this module is the reusable generalization.

| Module | Contents |
|---|---|
| `provider.py` | 4-family raw-HTTP provider layer (Anthropic native; OpenAI/DeepSeek/DashScope OpenAI-compatible), PL3 JSONL logging via the shared `llm_call_logger`, retry/backoff policy, JSON parsing, append-only record I/O. Carries the July-2026 API gotchas (Anthropic 4.7+ rejects temperature — omitted and logged; gpt-5.x uses `max_completion_tokens`; thinking-tier extractors need `max_out >= 2000`). |
| `prism_b.py` | The PRISM-B stated-reading instrument: eight dimensions, frozen renderer/extractor prompt set, dimension parser. Changing prompt wording forks the instrument version. |
| `stats.py` | Distances (cosine/Euclidean/Mahalanobis), max-pairwise dispersion floors, seeded source-cluster bootstrap, Holm correction, participation ratio. |
| `concordance.py` | Operator/family concordance diagnostics (leave-one-out vector concordance; majority-pick disagreement) + the pre-registered mechanical exclusion rule (score > 3x median of others) + the pairwise-disagreement choice floor. |

Import pattern (per-campaign code inserts the module's parent on `sys.path`):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))  # the bundle's code/
from prism_core import provider, prism_b, stats, concordance
```

Keys via `bws run -- <wrapper.sh>` (never plaintext): `ANTHROPIC_API_KEY`,
`OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `DASHSCOPE_API_KEY`.
