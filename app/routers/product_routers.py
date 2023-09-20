import pika
from fastapi import APIRouter, status
from beanie import PydanticObjectId

from app.producer import get_rabbitmq_channel, close_rabbitmq_channel
from app.services import product
from app.schemas.order_schemas import ProductResponseSchema
from app.schemas.product_schema import UpProductSchema

router = APIRouter(prefix='/api/items', tags=['Item'])


@router.get('', status_code=status.HTTP_200_OK)
async def get_items() -> list[ProductResponseSchema]:
    return await product.get_all_items()


@router.get('/{item_id}', status_code=status.HTTP_200_OK)
async def get_item(item_id: PydanticObjectId) -> ProductResponseSchema:
    try:
        connection, channel = get_rabbitmq_channel()
        properties = pika.BasicProperties('get_product')
        prod = await product.get_item_by_id(item_id)
        channel.basic_publish(exchange='', routing_key='wallet', body=prod.json(), properties=properties)
        return prod
    except Exception as e:
        raise e
    finally:
        close_rabbitmq_channel(connection, channel)


@router.patch('/{item_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_item(item_id: PydanticObjectId, item: UpProductSchema) -> ProductResponseSchema:
    return await product.update_item_by_id(item_id, item)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: PydanticObjectId) -> None:
    return await product.delete_item_by_id(item_id)
