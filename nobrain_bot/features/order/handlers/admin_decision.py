import re
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from nobrain_bot.database.session import async_session
from nobrain_bot.database.CRUD.order_crud import update_order_status, get_order_by_id
from nobrain_bot.features.common.keyboards.main_menu import main_menu_kb
from nobrain_bot.features.order.states import DeclineStates, EditStates
from nobrain_bot.features.order.keyboards.desicions import client_confirm_kb


router = Router(name="admin_orders")


# ========================
# ✅ Принятие заказа
# ========================
@router.callback_query(F.data.startswith("accept:"))
async def accept_order(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.split(":")[1])
    async with async_session() as session:
        order = await update_order_status(session, order_id, status="accepted")

    await callback.message.edit_text(f"✅ Заказ #{order_id} принят.")
    # клиенту красивое сообщение + меню
    await bot.send_message(
        order.tg_user_id,
        "✅ Ваш заказ принят!\n\n"
        "🚀 Отлично, мы начинаем работу над вашим проектом.\n"
        "Менеджер всегда на связи. С любым вопросом обращайтесь к нему через кнопку в главном меню 📱",
    )
    await bot.send_message(
        order.tg_user_id,
        "Главное меню 👇\n\nP.S подписывайтесь на наш блог! 😉",
        reply_markup=main_menu_kb()
    )


# ========================
# ❌ Отказ от заказа
# ========================
@router.callback_query(F.data.startswith("decline:"))
async def decline_order_start(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split(":")[1])
    await state.update_data(order_id=order_id)
    await callback.message.answer("✏️ Укажите причину отказа:")
    await state.set_state(DeclineStates.WaitingReason)


@router.message(F.text, DeclineStates.WaitingReason)
async def decline_order_finish(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    order_id = data["order_id"]
    reason = message.text.strip()

    async with async_session() as session:
        order = await update_order_status(session, order_id, status="declined", decline_reason=reason)

    await message.answer(f"❌ Заказ #{order_id} отклонён.")
    await bot.send_message(order.tg_user_id, f"Ваш заказ #{order_id} отклонён.\nПричина: {reason}")
    await state.clear()


# ========================
# ✏️ Админ меняет условия
# ========================
@router.callback_query(F.data.startswith("edit:"))
async def edit_order_start(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split(":")[1])
    await state.update_data(order_id=order_id)
    await callback.message.answer("📅 Укажите новые сроки в формате: 01.01.2025 - 10.01.2025")
    await state.set_state(EditStates.WaitingDates)


@router.message(F.text, EditStates.WaitingDates)
async def edit_order_dates(message: Message, state: FSMContext):
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
    await message.answer("💰 Укажите новую стоимость (только число, в рублях):")
    await state.set_state(EditStates.WaitingBudget)


@router.message(F.text, EditStates.WaitingBudget)
async def edit_order_budget(message: Message, state: FSMContext):
    text = message.text.strip().replace(" ", "")
    if not text.isdigit():
        await message.answer("⚠️ Укажите сумму только числом, без символов. Пример: 50000")
        return

    budget = int(text)
    await state.update_data(budget=budget)
    await message.answer("🖊 Напишите комментарий для клиента (почему меняются сроки или сумма):")
    await state.set_state(EditStates.WaitingComment)


@router.message(F.text, EditStates.WaitingComment)
async def edit_order_comment(message: Message, state: FSMContext, bot: Bot):
    comment = message.text.strip()
    data = await state.get_data()
    order_id = data["order_id"]
    start_date, end_date = data["start_date"], data["end_date"]
    budget = data["budget"]

    async with async_session() as session:
        order = await get_order_by_id(session, order_id)

    await bot.send_message(
        order.tg_user_id,
        f"📑 Новые условия по вашему заказу #{order_id}:\n\n"
        f"Сроки: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}\n"
        f"Стоимость: {budget:,} ₽\n"
        f"💬 Комментарий менеджера: {comment}\n\n"
        "Согласны ли вы?",
        reply_markup=client_confirm_kb(order_id)
    )

    await message.answer(f"✏️ Новое предложение с комментарием по заказу #{order_id} отправлено клиенту.")
    await state.clear()
