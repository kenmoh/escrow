import decimal

from pydantic import BaseModel


class CreateProductSchema(BaseModel):
    name: str
    quantity: int
    description: str
    price: decimal.Decimal
    image_url: str
