from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from ..modeling import BaseDbModel, BaseResponse


class User(BaseDbModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    is_admin: bool = False


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignupResponse(BaseResponse):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class LoginResponse(BaseResponse):
    access_token: str
    refresh_token: str


class RefreshResponse(BaseResponse):
    access_token: str
