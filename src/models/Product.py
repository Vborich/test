from tortoise import fields, models
from src.models import User


class Product(models.Model):
    id = fields.UUIDField(pk=True, auto_generate=True)
    name = fields.CharField(max_length=256)
    price_rub = fields.DecimalField(max_digits=10, decimal_places=2)

    owner: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User', related_name='own_products', on_delete=fields.OnDelete.CASCADE
    )

    class Meta:
        table = 'products'
