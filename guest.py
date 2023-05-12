import sandbox
from sandbox.types import Err
import json

class Sandbox(sandbox.Sandbox):
    def eval(expression: str) -> str:
        try:
            return json.dumps(eval(expression))
        except Exception as e:
            raise Err(str(e))

    def exec(statements: str):
        try:
            exec(statements)
        except Exception as e:
            raise Err(str(e))
