# Component Sandbox Demo

This is an example of how to use
[`wasmtime-py`](https://github.com/bytecodealliance/wasmtime-py) and
[`componentize-py`](https://github.com/dicej/componentize-py) to execute
sandboxed Python code snippets from within a Python app.

## Prerequisites

* [`wasmtime-py`](https://github.com/bytecodealliance/wasmtime-py)
* [`componentize-py`](https://github.com/dicej/componentize-py)

```
pip install wasmtime componentize-py
```

## Running the demo

```
componentize-py -d wit -w sandbox componentize guest -o sandbox.wasm --stub-wasi
python3 -m wasmtime.bindgen sandbox.wasm --out-dir sandbox
python3 host.py "2 + 2"
```

## Examples

`host.py` accepts zero or more `exec` strings (e.g. newline-delimited
statements) followed by a final `eval` string (i.e. an expression).  Note that
any symbols you declare in an `exec` string must be explicitly added to the
global scope using `global`.  This ensures it is visible to subsequent `exec`
and `eval` strings.

```shell-session
 $ python3 host.py "2 + 2"
result: 4
 $ python3 host.py 'global foo
def foo(): return 42' 'foo()'
result: 42
```
