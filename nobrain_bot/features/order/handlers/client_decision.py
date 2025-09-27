import re
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from nobrain_bot.database.session import async_session
from nobrain_bot.database.CRUD.order_crud import update_order_status
from nobrain_bot.core.config import get_settings
from nobrain_bot.features.common.keyboards.main_menu import main_menu_kb
from nobrain_bot.features.order.states import ClientEditStates
from nobrain_bot.features.order.keyboards.desicions import admin_confirm_kb


router = Router(name="client_orders")
config = get_settings()


# ========================
# 👤 Клиент соглашается
# ========================
@router.callback_query(F.data.startswith("client_accept:"))
async def client_accept(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.split(":")[1])

    async with async_session() as session:
        await update_order_status(session, order_id, status="accepted")

    await callback.message.edit_text(
        "✅ Вы согласились с условиями!\n\n"
        "🚀 Отлично, мы начинаем работу над вашим проектом.\n"
        "Менеджер всегда на связи. С любым вопросом обращайтесь к нему через кнопку в главном меню 😉",
    )
    await callback.message.answer(
        "Главное меню 👇",
        reply_markup=main_menu_kb()
    )
    await bot.send_message(config.admin_id, f"✅ Клиент согласился с условиями по заказу #{order_id}.")


# ========================
# ✏️ Клиент предлагает новые условия
# ========================
@router.callback_query(F.data.startswith("client_edit:"))
async def client_edit_start(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split(":")[1])
    await state.update_data(order_id=order_id)
    await callback.message.answer("📅 Укажите ваши сроки в формате: 01.01.2025 - 10.01.2025")
    await state.set_state(ClientEditStates.WaitingDates)


@router.message(F.text, ClientEditStates.WaitingDates)
async def client_edit_dates(message: Message, state: FSMContext):
    text = message.text.strip()
    match = re.match(r"(\d{2}\.\d{2}\.\d{4})\s*-\s*(\d{2}\.\d{2}\.\d{4})", text)
    if not match:
        await message.answer("⚠️ Формат неверный. Введите в виде: 01.01.2025 - 10.01.2025")
        return

    try:
        start_date = datetime.strptime(match.group(1), "%d.%m.%Y")
        end_date = datetime.strptime(match.group(2), "%d.%m.%Y")
        if end_date <= start_date:
            raise ValueError("end before start")
    except Exception:
        await message.answer("⚠️ Ошибка в датах. Убедитесь, что конец позже начала.")
        return

    await state.update_data(start_date=start_date, end_date=end_date)
    await message.answer("💰 Укажите ваш бюджет (только число, в рублях):")
    await state.set_state(ClientEditStates.WaitingBudget)


@router.message(F.text, ClientEditStates.WaitingBudget)
async def client_edit_budget(message: Message, state: FSMContext, bot: Bot):
    text = message.text.strip().replace(" ", "")
    if not text.isdigit():
        await message.answer("⚠️ Укажите сумму только числом, без символов. Пример: 50000")
        return

    budget = int(text)
    data = await state.get_data()
    order_id = data["order_id"]
    start_date, end_date = data["start_date"], data["end_date"]

    await bot.send_message(
        config.admin_id,
        f"🔄 Клиент предлагает новые условия по заказу #{order_id}:\n"
        f"Сроки: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}\n"
        f"Бюджет: {budget:,} ₽",
        reply_markup=admin_confirm_kb(order_id)
    )

    await message.answer(
        "✏️ Ваше предложение отправлено менеджеру.\n"
        ""
    )
    await state.clear()
