import bcrypt
from fastapi import HTTPException
from http import HTTPStatus
from psycopg2.extensions import connection
from schemas.register_schema import RegisterResponse, RegisterRequest
from utils.jwts import get_password_hash
import logging

# ロガーの設定
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,  # 開発時はDEBUG、本番はINFOなどに設定
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class RegisterService:
    """
    目的：
    引数のusername, emailを使い、データベースのusersテーブルに同じusernameとemailがないかを調べる
    """

    def _check_duplicate_credentials(conn: connection, username: str, email: str):
        logger.debug("START: _check_duplicate_credentials()")
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
            logger.debug("cur.execute()")
            result = cur.fetchone()  # 1行取得
            logger.debug("cur.fetchone()")

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
        logger.debug("END: _check_duplicate_credentials()")

    """
    目的： username,email,passwordを使い、新規ユーザーを作成
    """

    def _create_user(conn: connection, username: str, email: str, password: str) -> int:
        query = """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id
            """

        logger.debug("START: _create_user()")
        with conn.cursor() as cur:
            cur.execute(
                query,
                (username, email, password),
            )
            logger.debug("cur.execute()")
            result = cur.fetchone()
            logger.debug("cur.fetchone()")
            logger.debug("END: _create_user()")
            return result["id"]

    @staticmethod  # インスタンス化不要で呼び出せるmethod
    def register(conn: connection, register_data: RegisterRequest) -> dict:
        logger.debug("START: register()")
        # usernameとemailの重複をCheck
        RegisterService._check_duplicate_credentials(
            conn,
            register_data.username,
            register_data.email,
        )

        hashed = get_password_hash(register_data.password)

        # Create user
        _ = RegisterService._create_user(
            conn,
            register_data.username,
            register_data.email,
            hashed,
        )

        logger.debug("END: register()")
        return RegisterResponse(
            message="User created successfully. Please check your email to verify your account.",
        )
