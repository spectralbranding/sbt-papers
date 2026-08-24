# R16 companion computation

`cosine_null.py` computes the reference values the paper quotes when reading the
companion study's cross-model cosine similarity of .977: the same observed
profile against a uniform allocation, the mean cosine between independently
drawn allocations under two Dirichlet priors, and the two observed profiles
against each other.

Inputs are the published mean weight allocations of the companion study
(its Tables 4 and 5), reproduced inside the script. No network access and no
proprietary data are required.

```
uv run --with numpy python cosine_null.py
```

Fixed seed: `SEED = 42`. Dependencies: Python 3.12, numpy.
