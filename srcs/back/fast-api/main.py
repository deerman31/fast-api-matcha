from fastapi import FastAPI, Depends
from http import HTTPStatus
from db.database import get_db
from services.register_service import RegisterService
from schemas.register_schema import RegisterResponse, RegisterRequest

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello,World"}


@app.post("/api/auth/register",response_model=RegisterResponse,status_code=HTTPStatus.CREATED)
async def register(register_data: RegisterRequest, conn=Depends(get_db)):
    return RegisterService.register(conn, register_data)