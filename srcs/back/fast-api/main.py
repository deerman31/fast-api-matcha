from fastapi import FastAPI, Depends
from fastapi import HTTPException
from pydantic import ValidationError
from http import HTTPStatus
from db.database import get_db
from services.register_service import RegisterService
from schemas.register_schema import RegisterResponse, RegisterRequest

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello,World"}


@app.post("/api/auth/register", response_model=RegisterResponse)
async def register(register_data: RegisterRequest, conn=Depends(get_db)):
    try:
        return RegisterService.register(conn, register_data)
    except ValidationError as e:
        # ValidationErrorをHTTPExceptionに変換
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
