from fastapi import FastAPI, Depends, HTTPException
from http import HTTPStatus
from db.database import get_db
from services.register_service import RegisterService
from services.login_service import LoginService
from schemas.register_schema import RegisterResponse, RegisterRequest
from schemas.login_schema import LoginRequest, LoginResponse

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello,World"}


@app.post(
    "/api/auth/register",
    response_model=RegisterResponse,
    status_code=HTTPStatus.CREATED,
)
async def register(data: RegisterRequest, conn=Depends(get_db)):
    try:
        return RegisterService.register(conn, data)
    except HTTPException:
        raise
    except Exception as _:
        # 予期せぬエラーも500エラーとして処理
        # logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@app.post("/api/auth/login", response_model=LoginResponse, status_code=HTTPStatus.OK)
async def login(data: LoginRequest, conn=Depends(get_db)):
    try:
        return LoginService.login(conn, data)
    except HTTPException:
        raise
    except Exception as _:
        # 予期せぬエラーも500エラーとして処理
        # logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
