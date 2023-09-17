import decimal

from beanie import Document, Indexed, Link
from pydantic import Field


class Product(Document):
    name: Indexed(str)
    description: str
    quantity: int = Field(ge=1)
    price: decimal.Decimal = Field(decimal_places=2)
    image_url: str

    class Settings:
        name = 'products'


class Order(Document):
    order_name: Indexed(str)
    total_cost: decimal.Decimal
    merchant_id: str | None = None
    merchant_wallet_id: str | None = None
    merchant_name: str | None = None
    customer_wallet_id: str | None = None
    customer_full_name: str | None = None
    products: list[Link[Product]]

    class Settings:
        name = 'orders'
