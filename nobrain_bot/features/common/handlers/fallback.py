from aiogram import Router
from aiogram.types import Message

from nobrain_bot.features.common.keyboards.main_menu import main_menu_kb

router = Router(name="fallback")


@router.message()
async def fallback(message: Message):
    await message.answer(
        text=(
            "😕 Я вас не понял.\n"
            "Выберите, пожалуйста, действие через меню ниже 👇"
        ),
        reply_markup=main_menu_kb()
    )
