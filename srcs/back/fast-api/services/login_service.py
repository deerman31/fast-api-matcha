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
from services.err import USER_NOT_FOUND, INVALID_PASSWORD, EMAIL_NOT_VARIFY


class LoginService:
    @staticmethod
    def login(conn: connection, data: LoginRequest) -> dict:
        print("1----------------------------------------")
        user = get_user(conn, data.username)
        print("2----------------------------------------")
        if user is None:
            print("3----------------------------------------")
            raise HTTPException(
                status_code=USER_NOT_FOUND.status_code,
                detail=USER_NOT_FOUND.message,
            )
        print("4---------------------------------------")

        if not user.is_registered:
            raise HTTPException(
                status_code=EMAIL_NOT_VARIFY.status_code,
                detail=EMAIL_NOT_VARIFY.message,
            )
        print("5---------------------------------------")

        if not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=INVALID_PASSWORD.status_code,
                detail=INVALID_PASSWORD.message,
            )
        print("6---------------------------------------")

        expires = get_access_token_expires()
        access_token = create_access_token(data={"sub": user.id}, expires_delta=expires)

        if not LoginService._update_status_on(conn, user.id):
            raise HTTPException(
                status_code=USER_NOT_FOUND.status_code, detail=USER_NOT_FOUND.message
            )

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

        with conn.cursor() as cur:
            cur.execute(query, (id,))
            result = cur.fetchone()

            if result is None:
                return False
        return True
