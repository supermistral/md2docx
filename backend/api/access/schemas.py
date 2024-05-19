from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, SecretStr

from ..modeling import BaseDbModel, BaseResponse


class User(BaseDbModel):
    email: EmailStr
    password: SecretStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    is_admin: bool = False


class SignupRequest(BaseModel):
    email: EmailStr
    password: SecretStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class SignupResponse(BaseResponse):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
