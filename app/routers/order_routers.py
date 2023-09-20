import pika
from fastapi import APIRouter, status
from beanie import PydanticObjectId
from app.schemas.order_schemas import CreateOrderSchema, OrderResponseSchema, UpdateOrderSchema
from app.models.models import Order
from app.services import order
from app.producer import get_rabbitmq_channel, close_rabbitmq_channel


router = APIRouter(prefix='/api/orders', tags=['Orders'])


@router.get('', status_code=status.HTTP_200_OK)
async def get_all_orders() -> list[Order]:

    return await order.get_orders()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_new_order(order_schema: CreateOrderSchema) -> OrderResponseSchema:
    return await order.add_order(order_schema)


# noinspection PyUnboundLocalVariable
@router.get('/{order_id}', status_code=status.HTTP_200_OK)
async def get_order(order_id: PydanticObjectId) -> OrderResponseSchema:
    try:
        connection, channel = get_rabbitmq_channel()
        db_order = await order.get_single_order(order_id)
        properties = pika.BasicProperties('get_order')
        channel.basic_publish(exchange='', routing_key='wallet', body=db_order.json(), properties=properties)
        return db_order
    except Exception as e:
        raise e
    finally:
        # Close the RabbitMQ channel and connection
        close_rabbitmq_channel(connection, channel)


@router.patch('/{order_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_order(order_id: PydanticObjectId, order_schema: UpdateOrderSchema) -> UpdateOrderSchema:
    return await order.order_update(order_id, order_schema)


@router.delete('/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(merchant_id: str, order_id: PydanticObjectId) -> None:
    return await order.delete_order_by_id(merchant_id, order_id)


@router.get('/users/{merchant_id}', status_code=status.HTTP_200_OK)
async def get_user_orders(merchant_id: str) -> list[Order]:
    return await order.get_orders_by_user(merchant_id)
