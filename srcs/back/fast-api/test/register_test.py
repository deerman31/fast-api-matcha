from fastapi.testclient import TestClient
from schemas.register_schema import RegisterRequest


from main import app

# PYTHONPATH=/app pytest

client = TestClient(app)


# usernameが短い
def test_username_validate_err_short():
    username = "te"
    email = "test@test.com"
    password = "Oinari0618!"
    re_password = "Oinari0618!"
    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "username"],
                "msg": "Value error, Username must be at least 3 characters and no more than 20 characters",
                "input": username,
                "ctx": {"error": {}},
            }
        ]
    }


# usernameが長い
def test_username_validate_err_long():
    username = "test012345test012345test012345"
    email = "test@test.com"
    password = "Oinari0618!"
    re_password = "Oinari0618!"
    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "username"],
                "msg": "Value error, Username must be at least 3 characters and no more than 20 characters",
                "input": username,
                "ctx": {"error": {}},
            }
        ]
    }


# usernameに許可されていない記号が入っている
def test_username_err_disallowed_symbols():
    username = "test!"
    email = "test@test.com"
    password = "Oinari0618!"
    re_password = "Oinari0618!"
    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "username"],
                "msg": "value is not a valid email address: The part after the @-sign is not valid. It should have a period.",
                "input": username,
                "ctx": {"error": {}},
            }
        ]
    }


def test_email_err():
    username = "test"
    email = "test@tes"
    password = "Oinari0618!"
    re_password = "Oinari0618!"
    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "email"],
                "msg": "value is not a valid email address: The part after the @-sign is not valid. It should have a period.",
                "input": email,
                "ctx": {
                    "reason": "The part after the @-sign is not valid. It should have a period."
                },
            }
        ]
    }


# passwordに入れるべき記号がない
def test_password_err_symbol_not_included():
    username = "test"
    email = "test@test.com"
    password = "Oinari0618"
    re_password = "Oinari0618!"
    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "password"],
                "msg": "Value error, Password must contain at least one lowercase letter, one uppercase letter, one number and one special character",
                "input": password,
                "ctx": {"error": {}},
            }
        ]
    }


# paswordに英大文字がない
def test_password_err_capital_letters_not_included():
    username = "test"
    email = "test@test.com"
    password = "oinari0618!"
    re_password = "Oinari0618!"

    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "password"],
                "msg": "Value error, Password must contain at least one lowercase letter, one uppercase letter, one number and one special character",
                "input": password,
                "ctx": {"error": {}},
            }
        ]
    }


# paswordに英小文字がない
def test_password_err_lowercase_letters_not_included():
    username = "test"
    email = "test@test.com"
    password = "OINARI0618!"
    re_password = "Oinari0618!"

    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "password"],
                "msg": "Value error, Password must contain at least one lowercase letter, one uppercase letter, one number and one special character",
                "input": password,
                "ctx": {"error": {}},
            }
        ]
    }


# paswordに数字がない
def test_password_err_numbers_not_included():
    username = "test"
    email = "test@test.com"
    password = ("OinariOinari!",)
    re_password = "Oinari0618!"

    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "password"],
                "msg": "Value error, Password must contain at least one lowercase letter, one uppercase letter, one number and one special character",
                "input": password,
                "ctx": {"error": {}},
            }
        ]
    }


# passwordとre_passwordがmismatch
def test_password_err_mismatch():
    username = "test"
    email = "test@test.com"
    password = "Oinari0618!"
    re_password = "Oinari0618!mismatch"

    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "re_password"],
                "msg": "Value error, Password and confirm password do not match",
                "input": re_password,
                "ctx": {"error": {}},
            }
        ]
    }


def test_success():
    username = "ykusano"
    email = "ykusano@test.com"
    password = "Oinari0618!"
    re_password = "Oinari0618!"
    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)
    assert response.status_code == 201
    assert response.json() == {
        "message": "User created successfully. Please check your email to verify your account."
    }


# コンフリクトのtest
def test_username_conflict():
    username = "ykusano"
    email = "ykusano1@test.com"
    password = "Oinari0618!"
    re_password = "Oinari0618!"

    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)

    detail = f"Username {username} is already taken"
    assert response.status_code == 409
    assert response.json() == {"detail": detail}


# コンフリクトのtest
def test_email_conflict():
    username = "ykusano1"
    email = "ykusano@test.com"
    password = "Oinari0618!"
    re_password = "Oinari0618!"
    detail = f"Email {email} is already registered"

    request = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password,
    }

    response = client.post("/api/auth/register", json=request)

    assert response.status_code == 409
    assert response.json() == {"detail": detail}
