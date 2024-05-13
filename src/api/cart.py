import uuid

from fastapi import APIRouter, Depends

from src.application.cart.models.BaseProductModel import BaseProductModel
from src.application.cart.models.ProcessPaymentModel import ProcessPaymentModel
from src.application.cart.models.TotalCartAmount import TotalCartAmount
from src.application.cart.services.cartService import get_user_cart_products, add_product_to_user_cart, \
    remove_product_from_user_cart, process_user_cart_payment
from src.models.User import User
from src.application.auth.services.authService import JWTBearer

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.get("")
async def get_cart_products(current_user: User = Depends(JWTBearer())):
    return await get_user_cart_products(current_user)


@router.post("")
async def add_product_to_cart(product: BaseProductModel, current_user: User = Depends(JWTBearer())):
    return await add_product_to_user_cart(current_user, product.product_id)


@router.delete("")
async def remove_product_from_cart(product_id: uuid.UUID, current_user: User = Depends(JWTBearer())):
    return await remove_product_from_user_cart(current_user, product_id)


@router.post("/process-payment")
async def process_payment(payment: ProcessPaymentModel, current_user: User = Depends(JWTBearer())) -> TotalCartAmount:
    return await process_user_cart_payment(current_user, payment.product_ids)
