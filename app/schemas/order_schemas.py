from enum import Enum
from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class OrderStatus(str, Enum):
    PENDING = 'pending'
    DELIVERED = 'delivered'


class PaymentStatus(str, Enum):
    PENDING = 'pending'
    PAID = 'paid'


class CreateProductSchema(BaseModel):
    name: str
    quantity: int = Field(ge=1)
    description: str
    price: int = Field(gt=1)
    image_url: str


class ProductResponseSchema(CreateProductSchema):
    id: PydanticObjectId


class CreateOrderSchema(BaseModel):
    merchant_id: str
    merchant_wallet_id: str
    merchant_name: str
    customer_wallet_id: str | None = None
    customer_full_name: str | None = None
    order_name: str
    products: list[CreateProductSchema]


class UpdateOrderSchema(BaseModel):
    order_name: str


class UpdateCustomerOrderPaymentSchema(BaseModel):
    customer_wallet_id: str
    customer_full_name: str


class OrderResponseSchema(CreateOrderSchema):
    id: PydanticObjectId
    order_name: str
    total_cost: int
    payment_status: PaymentStatus
    order_status: OrderStatus


