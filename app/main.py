from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .schemas import ProductCreate, ProductResponse
from .telegram_webhook import bot, dp
from aiogram import types
from .crud import get_product_by_artikul, create_product, update_product
# from .scheduler import start_scheduler, schedule_product_update
import aiohttp

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # await start_scheduler()
    pass

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# Add the webhook endpoint
@app.post("/api/v1/webhook")
async def telegram_webhook(update: dict):
    telegram_event = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_event)
    return {"ok": True}

@app.post("/api/v1/products", response_model=ProductResponse)
async def create_product_endpoint(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    product_data = await fetch_product_data(product.artikul)
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_product = await get_product_by_artikul(db, product.artikul)
    if existing_product:
        # Update existing product with fresh data
        updated_product = await update_product(db, existing_product, product_data)
        return updated_product

    # Create new product if it doesn't exist
    new_product = await create_product(db, product_data)
    return new_product

# TODO: я не успел реализовать /api/v1/subscribe/{artikul} эндпоинт.
 
# @app.get("/api/v1/subscribe/{artikul}")
# async def subscribe_product_endpoint(artikul: int, db: AsyncSession = Depends(get_db)):
#     # await schedule_product_update(artikul, db)
#     return {"message": "Subscription started"}

async def fetch_product_data(artikul: int):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                # Extract the product information
                product = data['data']['products'][0]

                # Extract the required fields
                product_name = product['name']
                article_number = product['id']
                price = product['salePriceU'] / 100  # Assuming the price is in cents
                rating = product['rating']
                
                # Calculate the total quantity across all stocks
                total_quantity = sum(stock['qty'] for stock in product['sizes'][0]['stocks'])                

                product_data = {
                    'name': product_name,
                    'artikul': article_number,
                    'price': price,
                    'rating': rating,
                    'total_quantity': total_quantity
                }

                return product_data
    return None
