from fastapi import FastAPI

from app.database.database import init_db
from app.routers import order_routers

app = FastAPI(title="Escrow Service")


@app.on_event('startup')
async def connect_db():
    await init_db()


app.include_router(order_routers.router)
