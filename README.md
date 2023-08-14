# Component Sandbox Demo

This is an example of how to use
[`wasmtime-py`](https://github.com/bytecodealliance/wasmtime-py) and
[`componentize-py`](https://github.com/dicej/componentize-py) to execute
sandboxed Python code snippets from within a Python app.

## Prerequisites

* [`wasmtime-py`](https://github.com/bytecodealliance/wasmtime-py)
  * Until https://github.com/bytecodealliance/wasmtime-py/pull/171 is merged, use [this fork](https://github.com/dicej/wasmtime-py)
* [`componentize-py`](https://github.com/dicej/componentize-py) 0.3.0 or later

```
git clone https://github.com/dicej/wasmtime-py
(cd wasmtime-py && python ci/download-wasmtime.py && python ci/build-rust.py && pip install .)
pip install componentize-py
```

## Running the demo

```
componentize-py -d wit -w sandbox componentize guest -o sandbox.wasm
python3 -m wasmtime.bindgen sandbox.wasm --out-dir sandbox
python3 host.py "2 + 2"
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
