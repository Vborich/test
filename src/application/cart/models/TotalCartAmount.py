import decimal

from pydantic import BaseModel


class TotalCartAmount(BaseModel):
    total_rub: decimal.Decimal
    total_btc: decimal.Decimal
