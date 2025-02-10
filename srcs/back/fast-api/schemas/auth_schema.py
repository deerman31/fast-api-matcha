from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated

# カスタム型の定義
Username = Annotated[str, StringConstraints(min_length=1, max_length=255)]
Password = Annotated[str, StringConstraints(min_length=8, max_length=255)]


class RegisterRequest(BaseModel):
    username: Username
    email: EmailStr
    password: Password
    re_password: Password


class RegisterResponse(BaseModel):
    message: str | None
    error: str | None
