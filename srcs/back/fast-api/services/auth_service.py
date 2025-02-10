import bcrypt
from fastapi import HTTPException
from http import HTTPStatus
from psycopg2.extensions import connection
from schemas.auth_schema import RegisterResponse, RegisterRequest


class AuthService:
    @staticmethod
    def check_duplicate_credentials(conn: connection, username: str, email: str):
        with conn.cursor() as cur:
            cur.execute(
                """
            SELECT
                EXISTS(SELECT 1 FROM users WHERE username = %s) as username_exists,
                EXISTS(SELECT 1 FROM users WHERE email = %s) as email_exists
            """,
                (username, email),
            )
            result = cur.fetchone()

            if result["username_exists"]:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=f"Username {username} is already taken",
                )
            if result["email_exists"]:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=f"Email {email} is already registered",
                )

    @staticmethod
    def create_user(conn: connection, username: str, email: str, password: str) -> int:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id
            """,
                (username, email, password),
            )
            result = cur.fetchone()
            return result["id"]

    @staticmethod
    def register(conn: connection, register_data: RegisterRequest) -> dict:
        if register_data.password != register_data.re_password:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Password and confirm password do not match",
            )
        AuthService.check_duplicate_credentials(
            conn, register_data.username, register_data.email
        )

        # Hash password
        hashed = bcrypt.hashpw(
            register_data.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Create user
        user_id = AuthService.create_user(
            conn, register_data.username, register_data.email, hashed
        )
        return RegisterResponse(
            message="User created successfully. Please check your email to verify your account.",
            error=None,
        )
