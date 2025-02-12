from datetime import datetime, timedelta, timezone
from typing import Optional

from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from psycopg2.extensions import connection

from schemas.login_schema import LoginUser
import jwt

# 環境変数の読み込み
load_dotenv()

SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_LIMIT")
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 目的: 二つの引数を比較し、一致するかを調べる.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 目的: passwordをhash化する
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# 目的: usernameを使って、DBから該当のuser情報を取得する
def get_user(conn: connection, username: str) -> Optional[LoginUser]:
    query = """
        SELECT id, username, password_hash, is_online, is_registered, is_preparation
        FROM users 
        WHERE username = %s
        LIMIT 1
"""
    with conn.cursor() as cur:
        cur.execute(query, (username,))
        result = cur.fetchone()
        if result is None:
            return None

    return LoginUser(
        id=result["id"],
        username=result["username"],
        password_hash=result["password_hash"],
        is_online=result["is_online"],
        is_registered=result["is_registered"],
        is_preparation=result["is_preparation"],
    )


# access_tokenを生成
def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 上のcreate_access_token()に使うtokenの有効期限のexpiresを生成
def get_access_token_expires() -> timedelta:
    return timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
