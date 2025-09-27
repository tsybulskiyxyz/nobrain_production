from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from nobrain_bot.database.session import async_session
from nobrain_bot.database.CRUD.order_crud import create_order
from nobrain_bot.core.config import get_settings
from aiogram import Bot

from nobrain_bot.features.order.keyboards.desicions import admin_confirm_kb

router = Router(name="order_finalize")


async def finalize_order(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    async with async_session() as session:
        order = await create_order(
            session=session,
            tg_user_id=message.from_user.id,
            services=list(data.get("selected_services", [])),
            base_answers=data.get("base_answers", {}),
            details=data.get("details", {})
        )

    text = "📩 Новая заявка!\n\n"
    text += f"👤 Клиент: @{message.from_user.username or message.from_user.id}\n"
    text += f"🆔 Order ID: {order.id}\n"
    text += f"🛠 Услуги: {', '.join(data.get('selected_services', []))}\n\n"

    base = data.get("base_answers", {})
    if base:
        text += "📋 Общая информация:\n"
        for key, value in base.items():
            text += f"— {key}: {value}\n"
        text += "\n"

    details = data.get("details", {})
    for block, answers in details.items():
        text += f"🔹 {block.upper()}:\n"
        for k, v in answers.items():
            text += f"  • {k}: {v}\n"
        text += "\n"

    config = get_settings()
    try:
        await bot.send_message(config.admin_id, text=text, reply_markup=admin_confirm_kb(order.id))
    except Exception as e:
        print(f"Не удалось отправить админу {config.admin_id}: {e}")

    await message.answer(
        "✅ Ваш заказ сформирован и отправлен на обработку\n"
        "Мы скоро с вами свяжемся!"
    )
    await state.clear()
