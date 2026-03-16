# Paper Review: Spectral Brand Theory

**Reviewed**: 2026-03-16
**Paper**: `/Users/d/projects/sbt-papers/spectral-brand-theory/paper.md`
**Target venue**: Working Paper (Zenodo). No specific journal submission currently planned for the main SBT paper.
**Reviewer**: `/review-paper` automated adversarial protocol

---

## Q1: Overreach Check

### CRITICAL

(none)

### WARNING

- Line 77: "Our validation suggests it should be." — The word "validation" is used here to describe the five-brand demonstration's finding about the temporal dimension. Should be "Our demonstration suggests it should be" or "Our exploratory analysis suggests it should be." This is a remnant of pre-remediation language.

- Line 200: Table 3 caption reads "Five validation brands and selection rationale." — Should be "Five demonstration brands" or "Five case-study brands." Another "validation" remnant in a table heading.

- Line 219: "25 insights were assessed by the framework's author against four criteria; all 25 were judged to satisfy the criteria." — This is acknowledged as a limitation (single assessor), but the 100% pass rate (25/25) without any external blind assessment is a red flag for reviewers. The paper does acknowledge this ("Independent blind evaluation...would provide a stronger test"), which partially mitigates the concern. Still, a reviewer may ask why no insights failed any criteria.

- Line 438: "Our five-brand comparison tentatively suggests a possible optimal zone around 55-65% designed signals; this is an exploratory hypothesis requiring validation across a larger sample." — Uses "validation" but in the correct future-tense hedged sense. Acceptable, but note the word choice.

### NOTE

- The abstract's final disclaimer sentence ("The analyses constitute a structured demonstration...empirical validation against independently collected consumer data remains for future work") is well-crafted and appropriately hedged. This is the model for how all evidential claims should be framed.
- Line 36: "there is no single brand perception that applies uniformly to all observers" — This is a strong philosophical claim. The paper positions it as the core thesis, not as an empirical finding, which is appropriate.
- Line 481: The Peters (2019) ergodicity analogy is explicitly hedged as "an organizing framework — not as a claim that brand perception obeys the specific mathematical properties Peters demonstrates for wealth processes." Good epistemic discipline.

---

## Q2: Unstated Assumptions

### CRITICAL

(none)

### WARNING

- **Dimension selection (why 8, not 7 or 9?)**: Line 77 acknowledges dimensions "emerged from a synthesis of prior frameworks" and maps to Kapferer, Aaker, Holt. But the paper never defends WHY these 8 are complete or necessary. A reviewer will ask: "How do you know you haven't missed a dimension? What about functional/utilitarian dimensions (quality, reliability)? What about environmental/sustainability as a standalone dimension?" The paper treats the 8 dimensions as given after Section 2.2. A brief defense of completeness (or an explicit acknowledgment that 8 is a working set, not a proven exhaustive decomposition) would strengthen this.

- **LLM as proxy for human observers**: Lines 215, 229-241. The paper uses LLMs (Claude, Gemini) as the analytical engine. The cross-model replication is thorough (Table 7). But the unstated assumption is that LLM-based analysis produces insights structurally equivalent to what human expert analysts or consumer research would produce. Line 241 partially addresses this ("Testing the framework on brands with minimal public information would provide a stronger test") but the deeper assumption — that LLMs are valid instruments for this kind of perceptual analysis — is never explicitly defended. It is implicitly assumed by the "AI-native" framing.

- **Observer weight independence**: The spectral profile model (Section 2.3) treats dimensional weights as independent parameters. But perceptual dimensions may be correlated — an observer who weights "ideological" highly may systematically discount "economic" signals. The paper does not discuss potential weight correlations or their impact on cloud formation.

### NOTE

- Brand selection is well-defended (line 202 — chosen to "stress-test different properties"). The five brands cover a good architectural diversity. The limitation (well-known brands only) is explicitly acknowledged (line 243).
- The paper explicitly acknowledges snapshot-vs-longitudinal limitations (line 557) and weight validation limitations (line 553). These are self-aware and well-hedged.

---

## Q3: Generalizability Test

### CRITICAL

(none)

### WARNING

- **Western brand bias**: All five brands (Hermes, IKEA, Patagonia, Tesla, Erewhon) are Western-origin brands perceived through English-language media. The framework claims universality (8 dimensions for "brand perception") but has only been demonstrated on Western brands. A Chinese luxury brand (e.g., Shang Xia), a Japanese brand (e.g., Muji), or an Indian conglomerate (e.g., Tata) might reveal dimensions that don't map cleanly to the 8 — or might reveal that dimensional weights shift dramatically across cultures. This is not acknowledged as a limitation.

- **B2C exclusive**: All five brands are consumer-facing. B2B brands (e.g., Salesforce, McKinsey, BASF) have fundamentally different perception dynamics — fewer observers, longer decision cycles, committee-based evaluation, reputation vs experience balance. The paper never mentions B2B applicability. A reviewer from a marketing journal will notice this gap.

- **English-language analysis only**: The LLM analysis was conducted in English. Brand perception is linguistically mediated — the same brand may trigger different dimensional associations in different languages. This is not discussed.

### NOTE

- The paper's claims are appropriately scoped to "structured demonstration" rather than "general theory validated across all contexts." This hedging protects against most generalizability challenges.
- The 10 falsifiable hypotheses (Section 5.5) provide a clear research agenda. H1-H5 are well-specified with concrete test designs.

---

## Q4: Positioning in the Conversation

### CRITICAL

(none)

### WARNING

- **Hatch & Schultz (2010) missing**: The stakeholder co-creation tradition (Hatch & Schultz, "Toward a theory of brand co-creation," JBR 2010) is arguably the most direct precursor to SBT's "observer as co-creator" thesis. The paper cites Vargo & Lusch (2004) for value co-creation but does not engage with Hatch & Schultz's specific application to brand identity. A marketing reviewer will notice this absence.

- **Urde (2013) missing**: The "brand orientation" literature (Urde, "The corporate brand identity matrix," JBMS 2013) provides a structured approach to brand identity that partially overlaps with SBT's signal architecture. Not cited.

- **No engagement with consumer psychology**: The paper cites Festinger (1957), Damasio (1994), Kahneman (2011), and Krosnick & Petty (1995) — but these are foundational. No engagement with recent consumer psychology on brand perception: Park, MacInnis & Priester (2010, "Brand Attachment") or Thomson, MacInnis & Park (2005, "The Ties That Bind") on emotional brand connections. These would strengthen the observer model's psychological grounding.

### NOTE

- The paper does an excellent job positioning against Aaker (1996), Kapferer (2008), Keller (1993), Sharp (2010), and Vargo & Lusch (2004). Section 5.1 is one of the paper's strongest sections — it clearly articulates what SBT adds to each tradition.
- The Peters (2019) non-ergodicity connection is creative and well-hedged. It positions SBT at the intersection of brand theory and decision science, which is unusual and attention-getting.
- The Eco (1976) citation for structural absence is appropriate and shows semiotic depth.

---

## Q5: Missing Citations

### CRITICAL

(none)

### WARNING

- **Hatch, M. J., & Schultz, M. (2010)**: "Toward a theory of brand co-creation with implications for brand governance." *Journal of Brand Management*, 17(8), 590-604. The most direct precursor to observer-as-co-creator. Missing.

- **Urde, M. (2013)**: "The corporate brand identity matrix." *Journal of Brand Management*, 20(9), 742-761. Structured approach to brand identity dimensions. Missing.

- **Park, C. W., MacInnis, D. J., & Priester, J. R. (2010)**: "Brand attachment and brand attitude strength: Conceptual and empirical differentiation of two critical brand equity drivers." *Journal of Marketing*, 74(6), 1-17. Relevant to conviction formation. Missing.

- **Swaminathan, V., Stilley, K. M., & Ahluwalia, R. (2009)**: "When brand personality matters: The moderating role of attachment styles." *Journal of Consumer Research*, 35(6), 985-1002. Relevant to observer heterogeneity in brand perception. Missing.

### NOTE

- All self-citations (2026a-k) verified against CANONICAL_REFERENCES.md. All DOIs match. Citation keys are correct.
- All external citations appear to be real and correctly attributed (Aaker 1996, Kapferer 2008, Keller 1993, Peters 2019, etc.). No fabrication risk detected.
- The Peirce citation (1931-1958) is the standard Harvard collected papers reference. Correct.
- R7 (2026k) is cited in Section 3.5 and 5.4 — correct key.
- The MBA thesis citation (Zharnikov 2018) is in the Author Note, not the References section — this is appropriate (credential, not substantive citation).

---

## SBT-Specific Checks

### Terminology

| Term | Occurrences | Status |
|------|-------------|--------|
| "cohort" (not "segment") | Consistent throughout | PASS |
| "perception cloud" (not "brand image") | Used correctly; "brand image" appears only when describing Keller's framework or others' usage (line 382 in Tesla Boycotter context — "Their entire brand image is constructed from..." — this is the ONE instance that should be "perception" not "brand image") | WARNING — line 382 |
| "observer spectral profile" | Consistent | PASS |
| "re-collapse" (not "rebranding") | Consistent | PASS |
| "brand conviction" (not "brand attitude") | Consistent | PASS |

### Brand Profiles

Brand profiles are not presented as numeric vectors in the paper (they are in the framework doc and articles). The paper describes brands qualitatively through the case studies. No profile numbers to verify against canonical values.

### Citation Keys

All self-citation keys verified against CANONICAL_REFERENCES.md:
- 2026a (SBT) — not self-cited (this IS 2026a)
- 2026b (Alibi) — cited line 164. Correct.
- 2026c-g, 2026j (R0-R4, R6) — cited lines 251-261. All correct.
- 2026h (R5) — cited line 263. Correct.
- 2026i (OST) — cited line 263. Correct.
- 2026k (R7) — cited line 265, 567. Correct.

### Evidential Language

| Pattern | Occurrences | Status |
|---------|-------------|--------|
| "demonstrated" (for 5-brand analysis) | Abstract, Section 1, 3.1, 6 | PASS |
| "candidate mechanisms" (not "novel") | Abstract, Section 1, 4 | PASS |
| "structured demonstration" | Abstract, Section 6 | PASS |
| "exploratory analysis/hypothesis" | Section 4.2, 4.4 | PASS |
| **"validation"** (brand context) | Line 77, line 200 table caption | **WARNING** — 2 remnants |

---

## Summary

| Category | Critical | Warning | Note |
|----------|----------|---------|------|
| Q1 Overreach | 0 | 3 | 3 |
| Q2 Assumptions | 0 | 3 | 2 |
| Q3 Generalizability | 0 | 3 | 2 |
| Q4 Positioning | 0 | 3 | 3 |
| Q5 Citations | 0 | 4 | 5 |
| SBT Checks | 0 | 3 | 0 |
| **Total** | **0** | **19** | **15** |

**Recommendation**: **FIX WARNING ISSUES BEFORE NEXT ZENODO VERSION**

The paper has zero critical issues — the Session 52 remediation successfully addressed all overclaiming language in the abstract and methodology sections. The remaining 19 warnings fall into three categories:

1. **2 residual "validation" remnants** (lines 77, 200) — quick text fixes
2. **1 "brand image" terminology slip** (line 382) — quick text fix
3. **4 missing citations** (Hatch & Schultz, Urde, Park et al., Swaminathan et al.) — add to References and engage in Section 5.1
4. **3 unstated assumptions** (dimension completeness, LLM validity, weight independence) — add brief acknowledgments to Section 3.4 or 5.4
5. **3 generalizability gaps** (Western bias, B2C only, English only) — add to Section 3.4
6. **6 positioning/note items** — optional improvements

Priority for next revision: items 1-2 (text fixes, 5 minutes), then item 3 (missing citations, 30 minutes), then items 4-5 (assumption/generalizability acknowledgments, 30 minutes).

---

*Generated by `/review-paper` protocol. See `.claude/commands/review-paper.md` for methodology.*
