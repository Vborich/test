from tortoise import fields, models
from src.models import Product


class User(models.Model):
    id = fields.UUIDField(pk=True, auto_generate=True)
    username = fields.CharField(max_length=256, unique=True)
    password = fields.CharField(max_length=256)
    created_at = fields.DatetimeField(auto_now_add=True)

    own_products: fields.ReverseRelation[Product]
    cart_products = fields.ManyToManyField(
        model_name="models.Product", through="carts"
    )

    class Meta:
        table = "users"
