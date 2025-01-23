from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Product

async def get_product_by_artikul(db: AsyncSession, artikul: int):
    """
    Fetch a product from the database by its artikul.

    Args:
      db (AsyncSession): The database session to use for the query.
      artikul (int): The artikul of the product to fetch.

    Returns:
      Product: The product with the specified artikul, or None if no such product exists.
    """
    result = await db.execute(select(Product).where(Product.artikul == artikul))
    return result.scalars().first()

async def create_product(db: AsyncSession, product_data: dict):
    product = Product(**product_data)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product