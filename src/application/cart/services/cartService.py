import uuid

from binance import AsyncClient
from currency_converter import CurrencyConverter
from fastapi import HTTPException, status
from tortoise.expressions import Q

from src.application.cart.models.TotalCartAmount import TotalCartAmount
from src.models.Cart import Cart
from src.models.Product import Product
from src.models.User import User


async def get_user_cart_products(user: User):
    carts = await Cart.filter(user_id=user.id).select_related('product')
    return [cart.product for cart in carts]


async def add_product_to_user_cart(user: User, product_id: uuid.UUID):
    exist_product = await Product.filter(id=product_id).exists()

    if not exist_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with provided id does not exist",
        )

    has_cart_product = await Cart.filter(Q(product_id=product_id) & Q(user_id=user.id)).exists()

    if has_cart_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product has already been added to cart",
        )

    await Cart.create(product_id=product_id, user_id=user.id)


async def remove_product_from_user_cart(user: User, product_id: uuid.UUID):
    has_cart_product = await Cart.filter(Q(product_id=product_id) & Q(user_id=user.id)).exists()

    if not has_cart_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no product with provided id in the cart",
        )

    await Cart.filter(Q(product_id=product_id) & Q(user_id=user.id)).delete()


async def process_user_cart_payment(user: User, product_ids: list[uuid.UUID]) -> TotalCartAmount:
    carts_query = Cart.filter(Q(user_id=user.id) & Q(product_id__in=product_ids))
    carts = await carts_query.select_related('product')
    products = [cart.product for cart in carts]

    if len(products) != len(product_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no products with provided ids in the cart",
        )

    await carts_query.delete()

    total_amount_rub = sum([product.price_rub for product in products])
    total_amount_usd = CurrencyConverter().convert(total_amount_rub, 'RUB', 'USD')
    total_btc = await get_total_btc(total_amount_usd)

    return TotalCartAmount(total_rub=total_amount_rub, total_btc=total_btc)


async def get_total_btc(total_amount_usd: float) -> float:
    total_btc: float = 0

    client = await AsyncClient.create()

    try:
        avg_price = await client.get_avg_price(symbol='BTCUSDT')
        price = float(avg_price["price"])
        total_btc = round(total_amount_usd / price, 6)
    except Exception:
        pass
    finally:
        await client.close_connection()

    return total_btc
