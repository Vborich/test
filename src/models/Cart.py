from tortoise import fields, models


class Cart(models.Model):
    id = fields.UUIDField(pk=True, auto_generate=True)

    user = fields.ForeignKeyField(
        "models.User", on_delete=fields.OnDelete.CASCADE
    )
    product = fields.ForeignKeyField(
        "models.Product", on_delete=fields.OnDelete.CASCADE
    )

    class Meta:
        table = 'carts'
