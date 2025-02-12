from datetime import datetime, timedelta, timezone
from typing import Optional

from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from psycopg2.extensions import connection

from schemas.login_schema import LoginUser
import jwt
import logging

# ロガーの設定
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,  # 開発時はDEBUG、本番はINFOなどに設定
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# 環境変数の読み込み
load_dotenv()

SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_LIMIT")
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.debug("START: verify_password()")
    f = pwd_context.verify(plain_password, hashed_password)
    logger.debug("END: verify_password()")
    return f


def get_password_hash(password: str) -> str:
    logger.debug("START: get_password_hash()")
    f = pwd_context.hash(password)
    logger.debug("END: get_password_hash()")
    return f


def get_user(conn: connection, username: str) -> Optional[LoginUser]:
    query = """
        SELECT id, username, password_hash, is_online, is_registered, is_preparation
        FROM users 
        WHERE username = %s
        LIMIT 1
"""
    logger.debug("START: get_user()")
    with conn.cursor() as cur:
        logger.debug("OK: with conn.cursor() as cur:")
        cur.execute(query, (username,))
        logger.debug("OK: cur.execute()")
        result = cur.fetchone()
        logger.debug("OK: cur.fetchone()")
        if result is None:
            return None

    logger.debug("END: get_user()")
    return LoginUser(
        id=result["id"],
        username=result["username"],
        password_hash=result["password_hash"],
        is_online=result["is_online"],
        is_registered=result["is_registered"],
        is_preparation=result["is_preparation"],
    )


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    logger.debug("START: create_access_token()")
    to_encode = data.copy()
    logger.debug("OK: data.copy()")

    expire = datetime.now(timezone.utc) + expires_delta
    logger.debug("OK: datetime.now(timezone.utc) + expires_delta")
    to_encode.update({"exp": expire})
    logger.debug('OK: to_encode.update({"exp": expire})')
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug("OK: jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)")
    logger.debug("END: create_access_token()")
    return encoded_jwt


def get_access_token_expires() -> timedelta:
    logger.debug("START: get_access_token_expires()")
    t = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    logger.debug("END: get_access_token_expires()")
    return t
