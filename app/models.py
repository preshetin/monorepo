import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float


env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

DATABASE_URL_ASYNC = os.getenv("DATABASE_URL_ASYNC")

engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class Product(Base):
    """
    Represents a product in the database.

    Attributes:
        id (int): The primary key of the product.
        artikul (int): A unique identifier for the product.
        name (str): The name of the product.
        price (float): The price of the product.
        rating (float): The rating of the product.
        total_quantity (int): The total quantity of the product available.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    artikul = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    rating = Column(Float)
    total_quantity = Column(Integer)