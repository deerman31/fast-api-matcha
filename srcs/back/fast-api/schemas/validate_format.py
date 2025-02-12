from utils.validate_utils import is_pattern_match, length_check
from fastapi import HTTPException
from http import HTTPStatus
import re


def validate_username_format(username: str) -> str:
    if not length_check(username, 3, 20):
        raise ValueError(
            "Username must be at least 3 characters and no more than 20 characters"
        )
    pattern = "[a-zA-Z0-9_]"
    if not is_pattern_match(username, pattern):
        raise ValueError("Contains characters other than alphanumeric characters and _")
    return username


def validate_password_format(password: str) -> str:
    if not length_check(password, 8, 255):
        raise ValueError(
            "Password must be at least 8 characters and no more than 255 characters"
        )
    pattern = "[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]"
    if not is_pattern_match(password, pattern):
        raise ValueError(
            "Password must contain at least one lowercase letter, one uppercase letter, one number and one special character"
        )

    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_number = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password))

    if not (has_lower and has_upper and has_number and has_special):
        raise ValueError(
            "Password must contain at least one lowercase letter, one uppercase letter, one number and one special character"
        )

    return password
