import shutil
import subprocess

import pytest

import nimlang_lib_demo as demo


def py_fib(n):
    return n if n < 2 else py_fib(n - 1) + py_fib(n - 2)


def py_vandermonde(x, n=None):
    n = len(x) if n is None else n
    return [[float(xi) ** j for j in range(n)] for xi in x]


def test_fib_matches_python():
    assert [demo.fib(n) for n in range(20)] == [py_fib(n) for n in range(20)]


def test_vandermonde():
    assert demo.vandermonde([1.0, 2.0, 3.0]) == [[1, 1, 1], [1, 2, 4], [1, 3, 9]]


def test_vandermonde_columns():
    x = [0.5, -2.0, 3.0, 10.0]
    assert demo.vandermonde(x, 6) == py_vandermonde(x, 6)
    assert demo.vandermonde(x, 0) == [[], [], [], []]
    assert demo.vandermonde([]) == []


def test_vandermonde_accepts_ints():
    assert demo.vandermonde([2, 3], 3) == [[1, 2, 4], [1, 3, 9]]


def test_cli():
    exe = shutil.which("nimdemo")
    if exe is None:
        pytest.skip("nimdemo is not installed (editable installs do not build binaries)")
    out = subprocess.run([exe, "20"], capture_output=True, text=True, check=True).stdout
    assert out.strip() == "fib(20) = 6765"
