from aiogram import Router, F
from aiogram.types import Message
from nobrain_bot.core.config import get_settings
from nobrain_bot.features.common.keyboards.links import about_kb, blog_kb, manager_kb
from nobrain_bot.features.common.texts import ABOUT_TEXT, BLOG_TEXT, MANAGER_TEXT


router = Router(name="links")


@router.message(F.text == "🧠 Что такое nobrain_production?")
async def about_handler(message: Message):
    config = get_settings()
    await message.answer(text=ABOUT_TEXT, reply_markup=about_kb(config), parse_mode='Markdown')


@router.message(F.text == "📰 Наш канал")
async def blog_handler(message: Message):
    config = get_settings()
    await message.answer(text=BLOG_TEXT, reply_markup=blog_kb(config))


@router.message(F.text == "📱 Связаться с менеджером")
async def manager_handler(message: Message):
    config = get_settings()
    await message.answer(text=MANAGER_TEXT, reply_markup=manager_kb(config))