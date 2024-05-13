import uuid

import pytest
from httpx import AsyncClient
from tortoise.expressions import Q

from src.application.auth.services.authService import create_access_token
from src.models.Cart import Cart
from src.models.Product import Product
from src.models.User import User


@pytest.mark.asyncio
async def test_post_not_authenticated_user_403(client: AsyncClient):
    response = await client.post("/cart/process-payment", json={"product_ids": [3]})

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_post_authorized_user_without_provided_product_in_cart_400(client: AsyncClient):
    user = await User.create(**{"username": "vlad", "password": "12345678"})

    token = create_access_token({"id": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})

    response = await client.post("/cart/process-payment", json={"product_ids": [str(uuid.uuid4())]})

    assert response.status_code == 400
    assert response.json()["detail"] == "There is no products with provided ids in the cart"


@pytest.mark.asyncio
async def test_post_authorized_user_payment_processed_200(client: AsyncClient, mocker):
    user = await User.create(**{"username": "vlad", "password": "12345678"})
    product = await Product.create(**{"name": "test", "price_rub": 100}, owner=user)
    await Cart.create(user=user, product=product)

    mocked_total_btc = float(5)
    mocker.patch("src.application.cart.services.cartService.get_total_btc", return_value=mocked_total_btc)

    token = create_access_token({"id": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})

    response = await client.post("/cart/process-payment", json={"product_ids": [str(product.id)]})

    assert response.status_code == 200
    assert response.json() == {
        "total_rub": str(format(product.price_rub, ".2f")),
        "total_btc": str(mocked_total_btc)
    }

    assert await Cart.filter(Q(product_id=product.id) & Q(user_id=user.id)).count() == 0
