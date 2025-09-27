from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from nobrain_bot.features.common.texts import welcome
from nobrain_bot.features.common.keyboards.main_menu import main_menu_kb


router = Router(name="start")


@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer(text=welcome(message.from_user.first_name), parse_mode='Markdown', reply_markup=main_menu_kb())