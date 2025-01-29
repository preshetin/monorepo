from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_product_by_artikul, create_product
from .main import fetch_product_data

scheduler = AsyncIOScheduler()

async def update_product_data(artikul: int, db: AsyncSession):
    product_data = await fetch_product_data(artikul)
    if product_data:
        existing_product = await get_product_by_artikul(db, artikul)
        if existing_product:
            # Update existing product
            existing_product.name = product_data["name"]
            existing_product.price = product_data["price"]
            existing_product.rating = product_data["rating"]
            existing_product.total_quantity = product_data["total_quantity"]
            await db.commit()
        else:
            # Create new product
            await create_product(db, product_data)

async def schedule_product_update(artikul: int, db: AsyncSession):
    scheduler.add_job(update_product_data, IntervalTrigger(minutes=30), args=[artikul, db])

async def start_scheduler():
    scheduler.start()