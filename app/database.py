# from sqlalchemy.ext.asyncio import AsyncSession
# from .models import SessionLocal

# async def get_db() -> AsyncSession:
#     async with SessionLocal() as session:
#         yield session

        
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import AsyncGenerator
from .models import SessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session