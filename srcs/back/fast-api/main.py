from fastapi import FastAPI, Depends

from schemas.auth_schema import RegisterResponse, RegisterRequest

from db.database import get_db

from services.auth_service import AuthService

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello,World"}


@app.post("/auth/register", response_model=RegisterResponse)
async def register(register_data: RegisterRequest, conn=Depends(get_db)):
    return AuthService.register(conn, register_data)
