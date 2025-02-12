import bcrypt
from fastapi import HTTPException
from http import HTTPStatus
from psycopg2.extensions import connection
from schemas.register_schema import RegisterResponse, RegisterRequest


class RegisterService:
    def _check_duplicate_credentials(conn: connection, username: str, email: str):
        query = """
            SELECT
                EXISTS(SELECT 1 FROM users WHERE username = %s) as username_exists,
                EXISTS(SELECT 1 FROM users WHERE email = %s) as email_exists
            """

        with conn.cursor() as cur:
            # execute() sqlクエリを実行
            cur.execute(
                query,
                (username, email),
            )
            result = cur.fetchone()  # 1行取得

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

    def _create_user(conn: connection, username: str, email: str, password: str) -> int:
        query = """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id
            """

        with conn.cursor() as cur:
            cur.execute(
                query,
                (username, email, password),
            )
            result = cur.fetchone()
            return result["id"]

    @staticmethod  # インスタンス化不要で呼び出せるmethod
    def register(conn: connection, register_data: RegisterRequest) -> dict:
        # usernameとemailの重複をCheck
        RegisterService._check_duplicate_credentials(
            conn,
            register_data.username,
            register_data.email,
        )

        # Hash password
        hashed = bcrypt.hashpw(
            register_data.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Create user
        _ = RegisterService._create_user(
            conn,
            register_data.username,
            register_data.email,
            hashed,
        )

        return RegisterResponse(
            message="User created successfully. Please check your email to verify your account.",
        )
