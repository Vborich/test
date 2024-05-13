import pytest
from httpx import AsyncClient

from src.models.User import User


@pytest.mark.asyncio
async def test_post_user_not_exists_400(client: AsyncClient):
    data = {"username": "vvvv", "password": "123456"}

    response = await client.post("/auth/login", json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_post_user_with_valid_credentials_200(client: AsyncClient):
    data = {"username": "vlad", "password": "12345678"}
    await User.create(**data)

    response = await client.post("/auth/login", json=data)

    assert response.status_code == 200
    assert len(response.json()["access_token"]) > 10
