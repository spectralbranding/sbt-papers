# 2026r companion code

`reference_nulls.py` reproduces the three data-free reference nulls printed in the paper:
the random re-ranking mean absolute rank displacement (7.32 at n = 22, 100,000 draws), the
cosine reference (.993, 200,000 pairs) and the exchangeable variance-share null (100,000
draws). Seed 42, numpy `default_rng`. It asserts agreement with the printed values.

Run from the paper root (the folder that holds `paper.md` and `code/`):

    uv run --with numpy python code/reference_nulls.py

The within-model label permutation that would test RQ3 on the raw profile matrix is not
included.
