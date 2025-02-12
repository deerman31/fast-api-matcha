from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    ValidationInfo,
)
from schemas.validate_format import validate_username_format, validate_password_format


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    re_password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str) -> str:
        return validate_username_format(username)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, password: str) -> str:
        return validate_password_format(password)

    @field_validator("re_password")
    @classmethod
    def passwords_match(cls, re_password: str, info: ValidationInfo) -> str:
        re_password_validate = validate_password_format(re_password)

        if "password" not in info.data:
            raise ValueError("Password field is required")

        original_password = info.data["password"]
        if original_password != re_password_validate:
            raise ValueError("Password and confirm password do not match")

        return re_password


class RegisterResponse(BaseModel):
    message: str
