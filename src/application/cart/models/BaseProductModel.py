import uuid
from pydantic import BaseModel


class BaseProductModel(BaseModel):
    product_id: uuid.UUID
