import base64, json
from typing import Any

from fastapi import Request


def to_base64(s: Any) -> str:
    return base64.b64encode(json.dumps(s).encode('utf-8'))


def from_base64(s: str) -> Any:
    return json.loads(base64.b64decode(s))


def generate_created_by(request: Request) -> str:
    session_id = request.session.get("id")
    return f"anonymous:{session_id}"
