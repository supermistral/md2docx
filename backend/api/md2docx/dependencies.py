from fastapi import HTTPException, Request


async def verify_session(request: Request):
    session_id = request.session.get('id')
    if not session_id:
        raise HTTPException(400, detail="Session is incorrect")
