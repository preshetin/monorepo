import os
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

from app.crud import create_product, get_product_by_artikul, update_product
from app.fetch_product_data import fetch_product_data
from app.models import SessionLocal

load_dotenv()

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()
router = Router()

# Keyboard builder
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Получить данные по товару", 
        callback_data="get_product"
    ))
    return builder.as_markup()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Нажмите на кнопку, чтобы получить инфо по товару:",
        reply_markup=get_main_keyboard()
    )

@router.callback_query(lambda c: c.data == "get_product")
async def process_get_product(callback: CallbackQuery):
    await callback.message.answer("Введите артикул:")
    await callback.answer()

@router.message()
async def handle_article(message: Message):
    try:
        artikul = int(message.text)
        # Fetch product data from WB API
        product_data = await fetch_product_data(artikul)
        if not product_data:
            await message.answer("Товар не найден!", reply_markup=get_main_keyboard())
            return

        # Send message to user with data from API
        response = (
            f"{product_data['name']}\n\n"
            f"Артикул: {product_data['artikul']}\n"
            f"На всех складах: {product_data['total_quantity']} шт\n" 
            f"Рейтинг: {product_data['rating']}\n"
            f"Цена cо скидкой: {product_data['price']}₽"
        )
        await message.answer(response, reply_markup=get_main_keyboard())

        # Upsert product data to database
        async with SessionLocal() as db:
            existing_product = await get_product_by_artikul(db, artikul)
            if existing_product:
                await update_product(db, existing_product, product_data)
            else:
                await create_product(db, product_data)

    except ValueError:
        await message.answer("Введите правильный номер артикула!", reply_markup=get_main_keyboard())
    except Exception as e:
        await message.answer(f"Error: {str(e)}", reply_markup=get_main_keyboard())

# Register router
dp.include_router(router)
