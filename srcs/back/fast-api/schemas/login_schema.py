from pydantic import BaseModel, field_validator
from schemas.validate_format import validate_username_format, validate_password_format


class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str) -> str:
        return validate_username_format(username)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        return validate_password_format(password)


class LoginResponse(BaseModel):
    is_preparation: bool
    access_token: str


class LoginUser:
    id: int
    username: str
    password_hash: str
    is_online: bool
    is_registered: bool
    is_preparation: bool
