# R16: AI-Native Brand Identity

**Paper**: AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification

**Author**: Dmitry Zharnikov

**DOI**: [10.5281/zenodo.19391476](https://doi.org/10.5281/zenodo.19391476)

**Citation key**: 2026x

## Abstract

This paper proposes the observer-driven evolution thesis --- identity verification technologies change discontinuously in response to shifts in the observer type --- and introduces behavioral metamerism as the AI-native equivalent of visual brand confusion. It argues that cryptographic signatures on behavioral specifications (the Brand Function) are positioned to replace logos as the primary brand identity mechanism for AI-mediated commerce.

## Repository Contents

| File | Description |
|------|-------------|
| `paper.md` | Full paper (~9,300 words, 36 references, 6 propositions) |
| `behavioral_metamerism_pilot.py` | Empirical pilot study script for Proposition 6 |
| `requirements.txt` | Python dependencies for the pilot script |
| `CITATION.cff` | Citation metadata |

## Behavioral Metamerism Pilot

The pilot tests whether LLMs can distinguish brands with identical statistical profiles but different behavioral specifications. It implements the study design described in Section 9 of the paper.

### Quick Start (Demo Mode)

```bash
pip install -r requirements.txt
python behavioral_metamerism_pilot.py --demo
```

Demo mode uses simulated LLM responses to demonstrate the methodology and analysis pipeline. No API keys required.

### Live Execution

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GOOGLE_API_KEY=AI...

python behavioral_metamerism_pilot.py --live --runs 3 --output results.json --summary summary_tables.md
```

Live mode queries Claude, GPT, and Gemini with real brand discrimination prompts under two conditions:

- **Statistical-only**: LLM sees ratings, reviews, sentiment, claims
- **Specification-augmented**: LLM additionally sees verified Brand Function (return policy, dispute resolution, service failure communication, etc.)

### Measures

| Measure | What it tests |
|---------|--------------|
| **Brand discrimination** | Can the LLM distinguish brands that humans consider distinct? |
| **Behavioral prediction** | Does Brand Function access improve edge-case prediction accuracy? |
| **Recommendation stability** | Does Brand Function reduce cross-LLM recommendation variance? |
| **BMI (Behavioral Metamerism Index)** | Ratio of statistical similarity to behavioral difference (0 = no metamerism, 1 = maximum metamerism) |

### Statistical Tests

- Fisher's exact test on discrimination rate (statistical vs. augmented)
- Wilcoxon signed-rank test on confidence scores
- F-test (variance ratio) on cross-model stability
- Bootstrap 95% CI on BMI (1,000 samples)

### Custom Brands

Supply your own brands via YAML:

```bash
python behavioral_metamerism_pilot.py --live --brands my_brands.yaml
```

YAML format:

```yaml
profiles:
  - name: "BrandA"
    category: "Category"
    avg_rating: 4.3
    review_count: 12500
    price_range: "$25-45"
    key_claims: ["claim1", "claim2"]
    sentiment_summary: "positive"
  - name: "BrandB"
    ...

functions:
  - name: "BrandA"
    return_policy: "30-day no-questions refund"
    dispute_resolution: "..."
    supply_chain_disruption_response: "..."
    pricing_under_competition: "..."
    service_failure_communication: "..."
    edge_case_handling:
      out_of_stock_replacement: "..."
      expired_return_window: "..."
  - name: "BrandB"
    ...
```

## How to Cite

```bibtex
@article{zharnikov2026x,
  title={AI-Native Brand Identity: From Visual Recognition to Cryptographic Verification},
  author={Zharnikov, Dmitry},
  year={2026},
  doi={10.5281/zenodo.19391476},
  url={https://doi.org/10.5281/zenodo.19391476}
}
```

## License

MIT
