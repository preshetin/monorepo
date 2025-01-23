from pydantic import BaseModel

class ProductCreate(BaseModel):
    artikul: int

class ProductResponse(BaseModel):
    artikul: int
    name: str
    price: float
    rating: float
    total_quantity: int