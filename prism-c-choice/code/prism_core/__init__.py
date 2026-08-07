"""prism_core — shared machinery for the PRISM instrument family campaigns.

Extracted 2026-07-02 from the frozen 2026az campaign code
(code/, commit dc75b6f5) so PRISM-C/T reuse one module
instead of carrying copies. The 2026az code itself is NOT modified: it is
the published companion of a completed campaign and stays byte-stable.

Modules:
- provider    — 4-family raw-HTTP provider layer + PL3 logging + JSON parsing
- prism_b     — the PRISM-B stated-reading instrument (dimensions, renderer/
                extractor prompt set, dimension parser)
- stats       — distances, dispersion floors, seeded cluster bootstrap, Holm
- concordance — operator/family concordance diagnostics + the pre-registered
                exclusion rule evaluator
"""
