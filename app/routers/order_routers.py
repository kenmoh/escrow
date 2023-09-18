from fastapi import APIRouter, status
from beanie import PydanticObjectId
from app.schemas.order_schemas import CreateOrderSchema, OrderResponseSchema, UpdateOrderSchema
from app.models.models import Order
from app.services import order


router = APIRouter(prefix='/api/orders', tags=['Orders'])


@router.get('', status_code=status.HTTP_200_OK)
async def get_all_orders() -> list[Order]:
    return await order.get_orders()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_new_order(order_schema: CreateOrderSchema) -> OrderResponseSchema:
    return await order.add_order(order_schema)


@router.get('/{order_id}', status_code=status.HTTP_200_OK)
async def get_order(order_id: PydanticObjectId) -> OrderResponseSchema:
    return await order.get_single_order(order_id)


@router.patch('/{order_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_order(order_id: PydanticObjectId, order_schema: UpdateOrderSchema) -> UpdateOrderSchema:
    return await order.order_update(order_id, order_schema)


@router.delete('/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: PydanticObjectId) -> None:
    return await order.delete_order_by_name(order_id)
