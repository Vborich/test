import uuid

import pytest
from httpx import AsyncClient
from tortoise.expressions import Q

from src.application.auth.services.authService import create_access_token
from src.models.Cart import Cart
from src.models.Product import Product
from src.models.User import User


@pytest.mark.asyncio
async def test_delete_not_authenticated_user_403(client: AsyncClient):
    response = await client.delete("/cart", params={"product_id": 5})

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_delete_authorized_user_without_provided_product_in_cart_400(client: AsyncClient):
    user = await User.create(**{"username": "vlad", "password": "12345678"})

    token = create_access_token({"id": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})

    response = await client.delete("/cart", params={"product_id": str(uuid.uuid4())})

    assert response.status_code == 400
    assert response.json()["detail"] == "There is no product with provided id in the cart"


@pytest.mark.asyncio
async def test_delete_authorized_user_product_removed_from_cart_200(client: AsyncClient):
    user = await User.create(**{"username": "vlad", "password": "12345678"})
    product = await Product.create(**{"name": "test", "price_rub": 100}, owner=user)
    await Cart.create(user=user, product=product)

    token = create_access_token({"id": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})

    response = await client.delete("/cart", params={"product_id": str(product.id)})

    assert response.status_code == 200
    assert response.json() is None

    assert await Cart.filter(Q(product_id=product.id) & Q(user_id=user.id)).count() == 0
