import json
from typing import Any
from base64 import b64decode, b64encode
from itsdangerous import TimestampSigner

from ...config import settings


timestamp_signer = TimestampSigner(settings.SECRET_KEY)


def create_incorrect_session_cookie(key: str) -> str:
    return f"session={key}; Path=/; HttpOnly;"


def create_session_cookie(data: Any) -> str:
    data = b64encode(json.dumps(data).encode('utf-8'))
    data = timestamp_signer.sign(data).decode('utf-8')
    return data


def extract_session_cookie(set_cookie: str) -> Any:
    item = set_cookie.split(';')[0]
    key, value = item.split('=', maxsplit=1)
    data = timestamp_signer.unsign(value.encode('utf-8'))
    return {key: json.loads(b64decode(data))}
