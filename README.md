# Component Sandbox Demo

**Please note: This example is no longer being maintained.  Please see
https://github.com/bytecodealliance/componentize-py/tree/main/examples/sandbox
for an updated, maintained version.**

This is an example of how to use
[`wasmtime-py`](https://github.com/bytecodealliance/wasmtime-py) and
[`componentize-py`](https://github.com/dicej/componentize-py) to execute
sandboxed Python code snippets from within a Python app.

## Prerequisites

* [`wasmtime-py`](https://github.com/bytecodealliance/wasmtime-py) 12.0.0 or later
* [`componentize-py`](https://github.com/dicej/componentize-py) 0.4.2
* [WASI build of NumPy](https://github.com/dicej/wasi-wheels/releases)

```
pip install --upgrade componentize-py wasmtime
curl -OL https://github.com/dicej/wasi-wheels/releases/download/canary/numpy-wasi.tar.gz
tar xf numpy-wasi.tar.gz
```

## Running the demo

```
componentize-py -d wit -w sandbox componentize guest -o sandbox.wasm
python3 -m wasmtime.bindgen sandbox.wasm --out-dir sandbox
python3 host.py "numpy.matmul([[1, 2], [4, 5], [6, 7]], [[1, 2, 3], [4, 5, 6]]).tolist()"
```

## Examples

`host.py` accepts zero or more `exec` strings (e.g. newline-delimited
statements) followed by a final `eval` string (i.e. an expression).  Note that
any symbols you declare in an `exec` string must be explicitly added to the
global scope using `global`.  This ensures they are visible to subsequent `exec`
and `eval` strings.

```shell-session
 $ python3 host.py "2 + 2"
result: 4
 $ python3 host.py 'global foo
def foo(): return 42' 'foo()'
result: 42
```

### Time limit

`host.py` enforces a five second timeout on guest execution.  If and when the
timeout is reached, `wasmtime` will raise a `Trap` error.

```shell-session
 $ python3 host.py 'while True: pass' '1'
timeout!
Traceback (most recent call last):
  File "/Users/dicej/p/component-sandbox-demo/host.py", line 31, in <module>
    result = sandbox.exec(store, arg)
             ^^^^^^^^^^^^^^^^^^^^^^^^
...
```

### Memory limit

`host.py` limits guest memory usage to 20MB.  Any attempt to allocate beyond
that limit will fail.

```shell-session
 $ python3 host.py 'global foo
foo = bytes(100 * 1024 * 1024)' 'foo[42]'
exec error: MemoryError
```

### WASI-Virt

You can also use [`WASI-Virt`](https://github.com/bytecodealliance/WASI-Virt) to
wrap a component produced by `componentize-py`, e.g. to provide a virtual
filesystem.  However, as of this writing, `wasmtime-py` does not yet support the
compound components produced by `WASI-Virt`, so you'll need to use the Rust
version of `Wasmtime` to do it.

In the example below, we use `WASI-Virt` to wrap the guest component in a
virtual environment and then run it using a little app that's roughly the Rust
equivalent of the host.py script we used above.  Note that you'll need to
install [Rust](https://rustup.rs) to run this part.

```
cargo install --locked --git https://github.com/bytecodealliance/wasi-virt
wasi-virt sandbox.wasm -o sandbox-virt.wasm
cargo run --manifest-path runner/Cargo.toml --release -- sandbox-virt.wasm  \
    "numpy.matmul([[1, 2], [4, 5], [6, 7]], [[1, 2, 3], [4, 5, 6]]).tolist()"
```
