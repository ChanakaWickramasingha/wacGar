from sqlalchemy.orm import Session
from app.db.models import User
from app.core.security import hash_password
from app.routes.auth import get_db


def test_login_success(client, test_db):

    # create fake user
    user = User(
        username="amantha@gmail.com",
        password=hash_password("amantha")
    )

    test_db.add(user)
    test_db.commit()

    # correct login request
    response = client.post("/login", json={
        "username": "amantha@gmail.com",
        "password": "amantha"
    })

    assert response.status_code == 200
