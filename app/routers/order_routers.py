from fastapi import APIRouter, status

from app.schemas.order_schemas import CreateOrderSchema
from app.models.models import Order
from app.services import order


router = APIRouter(prefix='/api/orders', tags=['Orders'])


@router.get('', status_code=status.HTTP_200_OK)
async def get_all_orders() -> list[Order]:
    return await order.get_orders()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_new_order(new_order: CreateOrderSchema) -> Order:
    return await order.add_order(new_order)



