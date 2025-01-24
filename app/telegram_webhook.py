import os
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

from app.crud import get_product_by_artikul
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
        text="Get product data", 
        callback_data="get_product"
    ))
    return builder.as_markup()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Welcome! Click the button below to get product data:",
        reply_markup=get_main_keyboard()
    )

@router.callback_query(lambda c: c.data == "get_product")
async def process_get_product(callback: CallbackQuery):
    await callback.message.answer("Please enter the article number:")
    await callback.answer()

@router.message()
async def handle_article(message: Message):
    print(111)
    print(message)
    print(222)
    try:
        artikul = int(message.text)
        async with SessionLocal() as db:
            product = await get_product_by_artikul(db, artikul)
            if product:
                response = (
                    f"Product Information:\n"
                    f"Name: {product.name}\n"
                    f"Article: {product.artikul}\n"
                    f"Price: {product.price} RUB"
                )
                await message.answer(response, reply_markup=get_main_keyboard())
            else:
                await message.answer("Product not found!", reply_markup=get_main_keyboard())
    except ValueError:
        await message.answer("Please enter a valid article number!", reply_markup=get_main_keyboard())
    except Exception as e:
        await message.answer(f"Error: {str(e)}", reply_markup=get_main_keyboard())

# @app.post(f"/api/v1/webhook")
# async def telegram_webhook(update: dict):
#     telegram_event = types.Update(**update)
#     await dp.feed_update(bot=bot, update=telegram_event)
#     return {"ok": True}

# Register router
dp.include_router(router)