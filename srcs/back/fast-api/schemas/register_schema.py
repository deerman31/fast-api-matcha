from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    ValidationInfo,
)
from schemas.validate_format import validate_username_format, validate_password_format
import logging

# ロガーの設定
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,  # 開発時はDEBUG、本番はINFOなどに設定
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    re_password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str) -> str:
        logger.debug("START: validate_username()")
        v = validate_username_format(username)
        logger.debug("END: validate_username()")
        return v

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, password: str) -> str:
        logger.debug("START: validate_password_complexity()")
        v = validate_password_format(password)
        logger.debug("END: validate_password_complexity()")
        return v

    @field_validator("re_password")
    @classmethod
    def passwords_match(cls, re_password: str, info: ValidationInfo) -> str:
        logger.debug("START: passwords_match()")
        re_password_validate = validate_password_format(re_password)

        if "password" not in info.data:
            raise ValueError("Password field is required")

        original_password = info.data["password"]
        if original_password != re_password_validate:
            raise ValueError("Password and confirm password do not match")

        logger.debug("END: passwords_match()")
        return re_password


class RegisterResponse(BaseModel):
    message: str
