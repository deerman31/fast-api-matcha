from http import HTTPStatus
from dataclasses import dataclass


@dataclass
class ErrorMessage:
    status_code: int
    message: str


SUCCESS_REGISTER = ErrorMessage(
    status_code=HTTPStatus.OK,
    message="User created successfully. Please check your email to verify your account.",
)


DUPLICATE_USERNAME = ErrorMessage(
    status_code=HTTPStatus.CONFLICT,
    message="Username {} is already taken",
)

DUPLICATE_EMAIL = ErrorMessage(
    status_code=HTTPStatus.CONFLICT,
    message="Email {} is already taken",
)

USER_NOT_FOUND = ErrorMessage(
    status_code=HTTPStatus.NOT_FOUND,
    message="User not found",
)

INVALID_PASSWORD = ErrorMessage(
    status_code=HTTPStatus.FORBIDDEN,
    message="Invalid password",
)

EMAIL_NOT_VARIFY = ErrorMessage(
    status_code=HTTPStatus.FORBIDDEN,
    message="Email not verified",
)
