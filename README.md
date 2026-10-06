# uv-add-nimlang-lib-demo

A Python package whose core is written in Nim, built with
[nimlang](https://github.com/pietroppeter/uv-add-nimlang).

People who install it get prebuilt wheels: they need no Nim, no zig and no C compiler, and
neither `nimlang` nor `ziglang` is installed alongside it. nimlang is only a build-time
requirement. The repo is also an end-to-end test of that: CI builds every wheel from one Linux
machine, then installs and tests each one on its own OS.

## Use it

```sh
uv add nimlang-lib-demo
```

```python
from nimlang_lib_demo import fib, vandermonde

fib(30)                     # 832040
vandermonde([1, 2, 3])      # [[1.0, 1.0, 1.0], [1.0, 2.0, 4.0], [1.0, 3.0, 9.0]]
vandermonde([1, 2, 3], 4)   # 4 columns: powers 0 to 3
```

- `fib` is the naive recursion, a CPU-bound function where compiled code shines: `fib(27)`
  takes 2.6 ms here against 35 ms for the same Python.
- `vandermonde` builds the matrix with increasing powers, each column the previous one times
  `x`, as in the example from Jeff Bezanson's Julia thesis. It takes and returns plain Python
  lists, so the gain is small: 76 ms against 104 ms for a pure Python loop on a 1000 x 1000
  matrix, most likely because turning a million floats into Python objects dominates.

The wheel also installs a small Nim command-line tool:

```sh
nimdemo 30                  # fib(30) = 832040
```

## How it is built

`pyproject.toml` lists nimlang as a build requirement and points its hatch build hook at the
Nim sources:

```toml
[build-system]
requires = ["hatchling", "nimlang"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.nimlang]
extensions = ["src/nimlang_lib_demo/nimcore.nim"]  # importable as nimlang_lib_demo.nimcore
binaries = ["src/nimlang_lib_demo/nimdemo.nim"]  # installed as the `nimdemo` command

[tool.nimlang]
dependencies = ["nimpy"]
```

- `src/nimlang_lib_demo/nimcore.nim` exports procs to Python with
  [nimpy](https://github.com/yglukhov/nimpy).
- nimpy does not link against a specific Python, so one `py3-none-<platform>` wheel per
  platform covers every CPython 3 version.
- `NIMLANG_TARGET` cross-compiles through `zig cc`, so one Linux job builds the wheels for
  every platform (see [.github/workflows/ci.yml](.github/workflows/ci.yml)).

```sh
uv build                                         # wheel for this machine, plus the sdist
NIMLANG_TARGET=aarch64-macos uv build --wheel    # macOS arm64 wheel, from any OS
NIMLANG_TARGET=x86_64-windows-gnu uv build --wheel
```

Installing from the sdist instead of a wheel compiles the Nim code, so it pulls in nimlang
and needs network access for the nimble dependencies.

## Develop

```sh
uv sync            # editable install: builds the extension module next to its source
uv run pytest
```

Changing a `.nim` file triggers a rebuild on the next `uv run` (see `cache-keys` in
`pyproject.toml`). Editable installs do not build the `nimdemo` binary.

## Wheels

| Platform | Wheel tag |
|---|---|
| Linux x86_64 | `manylinux_2_17_x86_64` |
| Linux aarch64 | `manylinux_2_17_aarch64` |
| macOS arm64 | `macosx_11_0_arm64` |
| macOS x86_64 | `macosx_10_13_x86_64` |
| Windows x86_64 | `win_amd64` |

The macOS tags above need nimlang 0.0.2 or later. With 0.0.1 the binaries require macOS 13
while the tags claim older versions.
