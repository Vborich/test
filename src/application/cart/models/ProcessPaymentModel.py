import uuid

from pydantic import BaseModel


class ProcessPaymentModel(BaseModel):
    product_ids: list[uuid.UUID]
