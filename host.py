from sandbox import Root, RootImports
from sandbox.types import Ok, Err
from sandbox.imports import environment
from wasmtime import Config, Engine, Store
import json
import sys
from threading import Timer
from typing import List, Tuple

TIMEOUT_SECONDS = 20
MEMORY_LIMIT_BYTES = 20 * 1024 * 1024

class HostEnvironment(environment.HostEnvironment):
    def get_environment(self) -> List[Tuple[str, str]]:
        return []

    def get_arguments(self) -> List[str]:
        return []

args = sys.argv[1:]
if len(args) == 0:
    print("usage: python3 host.py [<statement>...] <expression>", file=sys.stderr)
    exit(-1)

config = Config()
config.epoch_interruption = True

def on_timeout(engine):
    print("timeout!")
    engine.increment_epoch()

engine = Engine(config)
timer = Timer(TIMEOUT_SECONDS, on_timeout, args=(engine,))
timer.start()

try:
    store = Store(engine)
    store.set_epoch_deadline(1)
    store.set_limits(memory_size=MEMORY_LIMIT_BYTES)

    sandbox = Root(
        store,
        RootImports(
            environment=HostEnvironment(),
            # As of this writing, `wasmtime-py` does not yet support WASI Preview 2,
            # and our example won't use it at runtime anyway, so we provide `None`
            # for most `wasi-cli` interfaces:
            poll=None,
            monotonic_clock=None,
            wall_clock=None,
            streams=None,
            types=None,
            preopens=None,
            random=None,
            exit=None,
            stdin=None,
            stdout=None,
            stderr=None,
            terminal_input=None,
            terminal_output=None,
            terminal_stdin=None,
            terminal_stdout=None,
            terminal_stderr=None
        )
    )
    for arg in args[:-1]:
        result = sandbox.exec(store, arg)
        if isinstance(result, Err):
            print(f"exec error: {result.value}")
            exit(-1)

    result = sandbox.eval(store, args[-1])
    if isinstance(result, Ok):
        result = json.loads(result.value)
        print(f"result: {result}")
    else:
        print(f"eval error: {result.value}")

finally:
    timer.cancel()
