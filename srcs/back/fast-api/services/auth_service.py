import bcrypt
from fastapi import HTTPException
from http import HTTPStatus
from psycopg2.extensions import connection
from schemas.auth_schema import RegisterResponse, RegisterRequest
import psycopg2.extrasimport psycopg2.extras


class AuthService:
    def _check_duplicate_credentials(conn: connection, username: str, email: str):icate_credentials(conn: connection, username: str, email: str):
        query = """"
            SELECT
                EXISTS(SELECT 1 FROM users WHERE username = %s) as username_exists,exists,
                EXISTS(SELECT 1 FROM users WHERE email = %s) as email_exists EXISTS(SELECT 1 FROM users WHERE email = %s) as email_exists
            """            """
ctory=psycopg2.extras.DictCursor) as cur:
        with conn.cursor() as cur:sername, email))
            # execute() sqlクエリを実行.fetchone()
            cur.execute("username_exists"]:
                query,n(
                (username, email),       status_code=HTTPStatus.CONFLICT,
            )name} is already taken",
            result = cur.fetchone()  # 1行取得                )

            if result["username_exists"]:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=f"Username {username} is already taken",
                )
            if result["email_exists"]:n, username: str, email: str, password: str) -> int:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=f"Email {email} is already registered",ALUES (%s, %s, %s)
                )                RETURNING id

    def _create_user(conn: connection, username: str, email: str, password: str) -> int:
        query = """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id (username, email, password),
            """            )
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:)
            cur.execute(query, (username, email, password))t["id"]
            result = cur.fetchone()
            return result["id"]
ter(conn: connection, register_data: RegisterRequest) -> dict:
    @staticmethod  # インスタンス化不要で呼び出せるmethod
    def register(conn: connection, register_data: RegisterRequest) -> dict:icate_credentials(
        # usernameとemailの重複をCheck            conn, register_data.username, register_data.email
        AuthService._check_duplicate_credentials(
            conn, register_data.username, register_data.email
        )

        # Hash passwordnsalt()
        hashed = bcrypt.hashpw(.decode("utf-8")
            register_data.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
create_user(
        # Create userd
        user_id = AuthService._create_user(
            conn, register_data.username, register_data.email, hashed
        )erResponse(
lly. Please check your email to verify your account.",
        return RegisterResponse(
            message="User created successfully. Please check your email to verify your account.",
            error=None,        )