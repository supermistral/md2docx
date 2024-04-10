from fastapi import Request


def generate_created_by(request: Request) -> str:
    session_id = request.session.get("id")
    return f"anonymous:{session_id}"
