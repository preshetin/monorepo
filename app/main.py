from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .schemas import ProductCreate, ProductResponse
from .crud import get_product_by_artikul, create_product
from .scheduler import start_scheduler, schedule_product_update
import aiohttp

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await start_scheduler()

@app.post("/api/v1/products", response_model=ProductResponse)
async def create_product_endpoint(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    existing_product = await get_product_by_artikul(db, product.artikul)
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists")

    product_data = await fetch_product_data(product.artikul)
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")

    new_product = await create_product(db, product_data)
    return new_product

@app.get("/api/v1/subscribe/{artikul}")
async def subscribe_product_endpoint(artikul: int, db: AsyncSession = Depends(get_db)):
    await schedule_product_update(artikul, db)
    return {"message": "Subscription started"}

async def fetch_product_data(artikul: int):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # Extract necessary fields from the response



                # Extract the product information
                product = data['data']['products'][0]
                # Extract the required fields
                product_name = product['name']
                article_number = product['id']
                price = product['priceU'] / 100  # Assuming the price is in cents
                rating = product['rating']
                # Calculate the total quantity across all stocks
                total_quantity = sum(stock['qty'] for stock in product['sizes'][0]['stocks'])                
                        # Create the product data object
                product_data = {
                    'name': product_name,
                    'artikul': article_number,
                    'price': price,
                    'rating': rating,
                    'total_quantity': total_quantity
                }

                return product_data
                
                

                # This is a placeholder, adjust according to the actual response structure
                product_info = data.get("data", {}).get("products", [])[0]
                return {
                    "artikul": artikul,
                    "name": product_info.get("name"),
                    "price": product_info.get("price"),
                    "rating": product_info.get("rating"),
                    "total_quantity": product_info.get("total_quantity")
                }
    return None