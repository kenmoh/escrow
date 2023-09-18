from pydantic import BaseModel, Field


class UpProductSchema(BaseModel):
    name: str
    quantity: int = Field(ge=1)
    description: str
    price: int = Field(ge=1)
    image_url: str
