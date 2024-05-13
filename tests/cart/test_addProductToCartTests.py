import pytest
from httpx import AsyncClient
from tortoise.expressions import Q

from src.application.auth.services.authService import create_access_token
from src.models.Cart import Cart
from src.models.Product import Product
from src.models.User import User


@pytest.mark.asyncio
async def test_post_not_authenticated_user_403(client: AsyncClient):
    response = await client.post("/cart", json={"product_id": 1})

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_post_authorized_user_with_product_exists_in_cart_400(client: AsyncClient):
    user = await User.create(**{"username": "vlad", "password": "12345678"})
    product = await Product.create(**{"name": "test", "price_rub": 100}, owner=user)
    await Cart.create(user=user, product=product)

    token = create_access_token({"id": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})

    response = await client.post("/cart", json={"product_id": str(product.id)})

    assert response.status_code == 400
    assert response.json()["detail"] == "Product has already been added to cart"


@pytest.mark.asyncio
async def test_post_authorized_user_product_added_to_cart_200(client: AsyncClient):
    user = await User.create(**{"username": "vlad", "password": "12345678"})
    product = await Product.create(**{"name": "test", "price_rub": 100}, owner=user)

    token = create_access_token({"id": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})

    response = await client.post("/cart", json={"product_id": str(product.id)})

    assert response.status_code == 200
    assert response.json() is None

    assert await Cart.filter(Q(product_id=product.id) & Q(user_id=user.id)).exists()
