import decimal

import pytest
from httpx import AsyncClient

from src.application.auth.services.authService import create_access_token
from src.models.Cart import Cart
from src.models.Product import Product
from src.models.User import User


@pytest.mark.asyncio
async def test_get_not_authenticated_user_403(client: AsyncClient):
    response = await client.get("/cart")

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_authorized_user_without_products_in_cart_200(client: AsyncClient):
    user = await User.create(**{"username": "vlad", "password": "12345678"})

    token = create_access_token({"id": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})

    response = await client.get("/cart")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_authorized_user_with_products_in_cart_200(client: AsyncClient):
    user = await User.create(**{"username": "vlad", "password": "12345678"})
    product = await Product.create(**{"name": "test", "price_rub": 100}, owner=user)
    await Cart.create(user=user, product=product)

    token = create_access_token({"id": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})

    response = await client.get("/cart")

    assert response.status_code == 200
    assert response.json() == [{
        "price_rub": decimal.Decimal(product.price_rub),
        "id": str(product.id),
        "name": product.name,
        "owner_id": str(user.id),
    }]
