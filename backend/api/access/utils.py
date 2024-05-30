import hashlib
import uuid


def check_password(input_value: str, db_value: str) -> bool:
    password, salt = db_value.split(":")
    return password == hashlib.sha256(salt.encode() + input_value.encode()).hexdigest()


def hash_password(input_value: str) -> str:
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(salt.encode() + input_value.encode()).hexdigest()
    return f"{hashed_password}:{salt}"
