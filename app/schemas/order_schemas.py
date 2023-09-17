import decimal

from pydantic import BaseModel
from beanie import PydanticObjectId


class CreateProductSchema(BaseModel):
    name: str
    quantity: int
    description: str
    price: decimal.Decimal
    image_url: str


class CreateOrderSchema(BaseModel):
    order_name: str
    products: list[CreateProductSchema]


class OrderResponseSchema(BaseModel):
    id: PydanticObjectId
    order_name: str


