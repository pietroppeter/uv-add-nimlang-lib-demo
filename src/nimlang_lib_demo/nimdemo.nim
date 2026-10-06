## A small command-line tool shipped in the wheel as `nimdemo`: prints fib(n).

import std/[os, strutils]

proc fib(n: int): int =
  if n < 2: n else: fib(n - 1) + fib(n - 2)

let n = if paramCount() > 0: parseInt(paramStr(1)) else: 30
echo "fib(", n, ") = ", fib(n)
