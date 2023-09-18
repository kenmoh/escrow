from beanie import Document, Indexed, Link
from pydantic import Field
from app.schemas.order_schemas import OrderStatus, PaymentStatus


class Product(Document):
    name: Indexed(str, unique=True)
    description: str
    quantity: int = Field(ge=1)
    price: int = Field(gt=1)
    image_url: str

    class Settings:
        name = 'products'


class Order(Document):
    order_name: Indexed(str, unique=True)
    order_status: OrderStatus = Field(default=OrderStatus.PENDING)
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    total_cost: int | None = None
    merchant_id: str | None = None
    merchant_wallet_id: str | None = None
    merchant_name: str | None = None
    customer_wallet_id: str | None = None
    customer_full_name: str | None = None
    products: list[Link[Product]]

    class Settings:
        name = 'orders'
