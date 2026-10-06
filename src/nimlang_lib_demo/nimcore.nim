## The compiled core of nimlang_lib_demo, exposed to Python through nimpy.

import nimpy

proc fib(n: int): int {.exportpy.} =
  ## Naive recursion on purpose: a CPU-bound function where Nim is far faster than Python.
  if n < 2: n else: fib(n - 1) + fib(n - 2)

proc vandermonde(x: seq[float], n: int = -1): seq[seq[float]] {.exportpy.} =
  ## Vandermonde matrix with increasing powers: row i is [1, x[i], x[i]^2, ..., x[i]^(n-1)].
  ## `n` columns, `len(x)` by default. Like the example in Bezanson's Julia thesis, each
  ## column is the previous one times `x`, so no power is computed from scratch.
  let cols = if n < 0: x.len else: n
  result = newSeq[seq[float]](x.len)
  for i, xi in x:
    result[i] = newSeq[float](cols)
    if cols > 0:
      result[i][0] = 1.0
    for j in 1 ..< cols:
      result[i][j] = result[i][j - 1] * xi
