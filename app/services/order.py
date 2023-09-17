from app.models.models import Order, Product
from app.schemas.order_schemas import CreateOrderSchema
from beanie import WriteRules


async def get_orders():
    """
    :return: List of orders in db
    """
    return await Order.find().to_list()


async def add_order(order: CreateOrderSchema):
    """
    :param order:
    :return: newly created order
    """
    new_order = Order(order_name=order.order_name)
    new_order.products = [
        Product(name=order.product.name, quantity=order.product.quantity, price=order.product.price, description=order.product.description, image_url=order.product.image_url)
    ]
    new_order.total_cost = sum([prod.price*prod.quantity for prod in new_order.products])
    return await new_order.save(link_rule=WriteRules.WRITE)
