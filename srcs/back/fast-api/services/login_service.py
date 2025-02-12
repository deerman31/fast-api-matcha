from psycopg2.extensions import connection
from schemas.login_schema import LoginRequest, LoginResponse
from http import HTTPStatus
from fastapi import HTTPException
from utils.jwts import (
    get_user,
    verify_password,
    get_access_token_expires,
    create_access_token,
)

import logging

# ロガーの設定
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,  # 開発時はDEBUG、本番はINFOなどに設定
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class LoginService:
    @staticmethod
    def login(conn: connection, data: LoginRequest) -> dict:
        logger.debug("START: login()")
        user = get_user(conn, data.username)
        if user is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not found",
            )

        logger.debug("OK get_user()")

        if not user.is_registered:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Email not verified",
            )
        logger.debug("user.is_registered")

        if not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Invalid password",
            )
        logger.debug("OK verify_password()")

        expires = get_access_token_expires()

        logger.debug("OK: get_access_token_expires()")

        access_token = create_access_token(data={"sub": user.id}, expires_delta=expires)
        logger.debug("OK: create_access_token()")

        if not LoginService._update_status_on(conn, user.id):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not found",
            )
        logger.debug("OK: _update_status_on()")

        logger.debug("OK: login()")
        return LoginResponse(
            is_preparation=user.is_preparation,
            access_token=access_token,
        )

    def _update_status_on(conn: connection, id: int) -> bool:
        query = """
        UPDATE users 
        SET is_online = TRUE 
        WHERE id = %s
        RETURNING id
        """

        logger.debug("START: _update_status_on()")

        with conn.cursor() as cur:
            logger.debug("OK: with conn.cursor() as cur:")
            cur.execute(query, (id,))
            logger.debug("OK: cur.execute(query, (id,))")
            result = cur.fetchone()
            logger.debug("OK: result = cur.fetchone()")

            logger.debug("OK: _update_status_on()")
            if result is None:
                return False
        return True
