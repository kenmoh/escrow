from fastapi import HTTPException, status
from app.schemas.order_schemas import CreateOrderSchema, UpdateOrderSchema
from beanie import WriteRules, PydanticObjectId, DeleteRules
from beanie.exceptions import RevisionIdWasChanged, DocumentNotFound
from app.models.models import Order, Product
from app.utils.utils import not_found_exception


async def get_orders():
    """
    :return: List of orders in db
    """
    return await Order.find(fetch_links=True).to_list()


async def add_order(order: CreateOrderSchema):
    """

    :param order:
    :return: newly created order
    """
    try:
        new_order = Order(
            order_name=order.order_name,

            products=[
                Product(
                    name=prod.name,
                    quantity=prod.quantity,
                    price=prod.price,
                    description=prod.description,
                    image_url=prod.image_url
                ) for prod in order.products
            ])

        new_order.total_cost = sum([prod.price*prod.quantity for prod in order.products])
        return await new_order.save(link_rule=WriteRules.WRITE)
    except RevisionIdWasChanged as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Product name already exist!')


async def get_single_order(order_id: PydanticObjectId):

    try:
        order = await Order.find_one(Order.id == order_id, fetch_links=True)
        if not order:
            not_found_exception(order_id, 'Order')
        return order
    except DocumentNotFound:
        not_found_exception(order_id, 'Order')


async def order_update(order_id: PydanticObjectId, order: UpdateOrderSchema):
    try:
        order_db = await Order.find_one(Order.id == order_id)
        if not order_db:
            not_found_exception(order_id, 'Order')
        order_db.order_name = order.order_name
        return await order_db.replace()
    except DocumentNotFound as e:
        not_found_exception(order_id, 'Order')


async def delete_order_by_name(order_id: PydanticObjectId):
    order = await Order.find_one(Order.id == order_id, fetch_links=True)
    if order is None:
        not_found_exception(order_id, 'Order')
    await order.delete(link_rule=DeleteRules.DELETE_LINKS)

