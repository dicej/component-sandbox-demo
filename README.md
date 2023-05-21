# Component Sandbox Demo

This is an example of how to use
[`wasmtime-py`](https://github.com/bytecodealliance/wasmtime-py) and
[`componentize-py`](https://github.com/dicej/componentize-py) to execute
sandboxed Python code snippets from within a Python app.

## Prerequisites

### [`wasmtime-py`](https://github.com/bytecodealliance/wasmtime-py)

```
pip install wasmtime
```

### [`componentize-py`](https://github.com/dicej/componentize-py)

As of this writing, `componentize-py` has not yet been packaged as a Python
library or command, so you can't use pip to install it.  I'm planning to address
that soon, but meanwhile you can grab the appropriate binary from GitHub.  Run
one of the following, depending on your OS and architecture:

Linux/x86_64:
```
curl -L https://github.com/dicej/componentize-py/releases/download/canary/componentize-py-canary-linux-amd64.tar.gz | tar xz
```
Linux/aarch64:
```
curl -L https://github.com/dicej/componentize-py/releases/download/canary/componentize-py-canary-linux-aarch64.tar.gz | tar xz
```
MacOS/x86_64:
```
curl -L https://github.com/dicej/componentize-py/releases/download/canary/componentize-py-canary-macos-amd64.tar.gz | tar xz
```
MacOS/aarch64:
```
curl -L https://github.com/dicej/componentize-py/releases/download/canary/componentize-py-canary-macos-aarch64.tar.gz | tar xz
```
Windows/x86_64:
```
curl -L https://github.com/dicej/componentize-py/releases/download/canary/componentize-py-canary-windows-amd64.tar.gz | tar xz
```

## Running the demo

```
./componentize-py -d wit -w sandbox componentize guest -o sandbox.wasm --stub-wasi
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
