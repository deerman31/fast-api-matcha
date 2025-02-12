from fastapi.testclient import TestClient
from schemas.register_schema import RegisterRequest


from main import app

client = TestClient(app)


def test_register():
    request = RegisterRequest(
        username="ykusano",
        email="ykusano@test.com",
        password="Oinari0618!",
        re_password="Oinari0618!",
    )

    response = client.post("/api/auth/register", json=request.dict())
    assert response.status_code == 200
    assert response.json() == {
        "message": "User created successfully. Please check your email to verify your account."
    }
