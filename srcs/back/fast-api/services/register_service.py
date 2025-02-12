from fastapi import HTTPException
from psycopg2.extensions import connection
from schemas.register_schema import RegisterResponse, RegisterRequest, Duplicate
from utils.jwts import get_password_hash
from services.err import (
    SUCCESS_REGISTER,
    DUPLICATE_USERNAME,
    DUPLICATE_EMAIL,
)


class RegisterService:
    # 目的: 引数のusername, emailを使い、データベースのusersテーブルに同じusernameとemailがないかを調べる
    def _check_duplicate_credentials(
        conn: connection, username: str, email: str
    ) -> Duplicate:
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
                return Duplicate.USERNAME
            if result["email_exists"]:
                return Duplicate.EMAIL
        return Duplicate.NONE

    # 目的： username,email,passwordを使い、新規ユーザーを作成
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
    def register(conn: connection, data: RegisterRequest) -> dict:
        # usernameとemailの重複をCheck
        match RegisterService._check_duplicate_credentials(
            conn, data.username, data.email
        ):
            case Duplicate.USERNAME:
                raise HTTPException(
                    status_code=DUPLICATE_USERNAME.status_code,
                    detail=DUPLICATE_USERNAME.message.format(data.username),
                )
            case Duplicate.EMAIL:
                raise HTTPException(
                    status_code=DUPLICATE_EMAIL.status_code,
                    detail=DUPLICATE_EMAIL.message.format(data.email),
                )

        hashed = get_password_hash(data.password)

        _ = RegisterService._create_user(conn, data.username, data.email, hashed)

        return RegisterResponse(message=SUCCESS_REGISTER.message)
