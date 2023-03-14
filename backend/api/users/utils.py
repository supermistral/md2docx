import base64
import json
from typing import Any


def to_base64(s: Any) -> str:
    return base64.b64encode(json.dumps(s).encode('utf-8'))


def from_base64(s: str) -> Any:
    return json.loads(base64.b64decode(s))
