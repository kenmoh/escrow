from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models.models import Product, Order


DB_URL = "mongodb+srv://kenmoh:areneth@cluster0.nctfshi.mongodb.net/?retryWrites=true&w=majority"


async def init_db(): 
    db = AsyncIOMotorClient(DB_URL)
    await init_beanie(database=db.escrow, document_models=[Product, Order])

