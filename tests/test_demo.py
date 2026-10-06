from nimlang_lib_demo import fast, slow


def test_fast_matches_slow():
    assert [fast.fib(n) for n in range(20)] == [slow.fib(n) for n in range(20)]
