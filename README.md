# uv-add-nimlang-lib-demo

A minimal Python package that ships a function compiled from Nim, built with
[nimlang](https://github.com/pietroppeter/uv-add-nimlang). People who install it get a
prebuilt wheel: no Nim, no zig, no C compiler, and neither nimlang nor ziglang gets installed.

> AI disclosure: this project is mostly vibed. Currently [level 7](https://www.visidata.org/blog/2026/ai/#level-6%3A-bots-coded%2C-human-understands-mostly) on visidata AI scale: Human specced, bots coded.

## Try it

```sh
uv run --with nimlang-lib-demo python -m timeit -s "from nimlang_lib_demo.slow import fib" "fib(30)"
uv run --with nimlang-lib-demo python -m timeit -s "from nimlang_lib_demo.fast import fib" "fib(30)"
```

## The whole package

```
pyproject.toml
src/nimlang_lib_demo/__init__.py   # empty
src/nimlang_lib_demo/slow.py       # fib in Python
src/nimlang_lib_demo/fast.nim      # fib in Nim, importable as nimlang_lib_demo.fast
nimlang.lock                       # pinned commit of nimpy, written by nimlang on the first build
```

`slow.py`:

```python
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

`fast.nim`:

```nim
import nimpy

proc fib(n: int): int {.exportpy.} =
  if n < 2: n else: fib(n - 1) + fib(n - 2)
```

`pyproject.toml`: nimlang is a build requirement only, and its hatch hook compiles `fast.nim`.

```toml
[project]
name = "nimlang-lib-demo"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = []

[build-system]
requires = ["hatchling", "nimlang>=0.0.2"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.nimlang]
extensions = ["src/nimlang_lib_demo/fast.nim"]

[tool.nimlang]
dependencies = ["nimpy"]
```

## Build it yourself

To reproduce from scratch, create the four source files above (for example after
`uv init --lib nimlang-lib-demo`), then:

```sh
uv run python -m timeit -s "from nimlang_lib_demo.fast import fib" "fib(30)"   # builds fast.so in place
uv build                                          # sdist + wheel for this machine
NIMLANG_TARGET=aarch64-macos uv build --wheel     # cross-build for another platform
```

The wheel is tagged `py3-none-<platform>`, so one wheel per platform covers every CPython 3.
Releases also include the sdist, only as a fallback for platforms without a wheel (musl Linux,
Windows on ARM): installing from it compiles `fast.nim` with nimlang in a temporary build
environment, so it is slower and needs network access, but nothing extra stays installed.
[CI](.github/workflows/ci.yml) builds the wheels for Linux, macOS and Windows on a single Linux
machine. It then installs each one on its own OS, with no nimlang or ziglang, and runs the
[test](tests/test_demo.py).
