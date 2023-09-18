from beanie.exceptions import DocumentNotFound
from beanie import PydanticObjectId
from app.models.models import Product
from app.utils.utils import not_found_exception
from app.schemas.product_schema import UpProductSchema


async def get_all_items():
    """
    :return: List of items from the db
    """
    return await Product.find().to_list()


async def get_item_by_id(item_id: PydanticObjectId):
    """

    :param item_id:
    :return: a single item from the db
    """

    try:
        item = await Product.find_one(Product.id == item_id)
        if not item:
            not_found_exception(item_id, 'Item')
        return item
    except DocumentNotFound as e:
        not_found_exception(item_id, 'Item')


async def update_item_by_id(item_id: PydanticObjectId, item: UpProductSchema):
    try:
        item_db: Product = await Product.find_one(Product.id == item_id)
        if not item_db:
            not_found_exception(item_id, 'Item')

        item_db.name = item.name
        item_db.description = item.description
        item_db.quantity = item.quantity
        item_db.image_url = item.image_url
        item_db.price = item.price

        return await item_db.replace()

    except DocumentNotFound as e:
        not_found_exception(item_id, 'Item')


async def delete_item_by_id(item_id: PydanticObjectId):
    """

    :param item_id:
    :return: None
    """

    try:
        item = await Product.find_one(Product.id == item_id)
        if not item:
            not_found_exception(item_id, 'Item')
        await item.delete()
    except DocumentNotFound as e:
        not_found_exception(item_id, 'Item')
