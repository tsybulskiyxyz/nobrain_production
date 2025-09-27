import re
from datetime import datetime, date
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from nobrain_bot.features.order.states import OrderStates
from nobrain_bot.features.order.utils import go_to_next_service_block


router = Router(name="order_base")


@router.message(OrderStates.Base_About)
async def base_about(message: Message, state: FSMContext):
    data = await state.get_data()
    base = data.get("base_answers", {})
    base["about"] = message.text.strip()
    await state.update_data(base_answers=base)
    await message.answer("👥 Кто ваша целевая аудитория?")
    await state.set_state(OrderStates.Base_Audience)


@router.message(OrderStates.Base_Audience)
async def base_audience(message: Message, state: FSMContext):
    data = await state.get_data()
    base = data.get("base_answers", {})
    base["audience"] = message.text.strip()
    await state.update_data(base_answers=base)
    await message.answer("🎯 Какая цель проекта?")
    await state.set_state(OrderStates.Base_Goal)


@router.message(OrderStates.Base_Goal)
async def base_goal(message: Message, state: FSMContext):
    data = await state.get_data()
    base = data.get("base_answers", {})
    base["goal"] = message.text.strip()
    await state.update_data(base_answers=base)
    await message.answer("⏱ Укажите сроки в формате: 01.01.2025 - 10.01.2025")
    await state.set_state(OrderStates.Base_Timing)


@router.message(OrderStates.Base_Timing)
async def base_timing(message: Message, state: FSMContext):
    text = message.text.strip()
    match = re.match(r"(\d{2}\.\d{2}\.\d{4})\s*-\s*(\d{2}\.\d{2}\.\d{4})", text)
    if not match:
        await message.answer("⚠️ Укажите сроки в формате: 01.01.2025 - 10.01.2025")
        return

    try:
        start_date = datetime.strptime(match.group(1), "%d.%m.%Y").date()
        end_date = datetime.strptime(match.group(2), "%d.%m.%Y").date()
        today = date.today()

        if start_date < today:
            await message.answer("⚠️ Дата начала не может быть в прошлом. Укажите актуальные сроки.")
            return
        if end_date <= start_date:
            await message.answer("⚠️ Дата окончания должна быть позже даты начала.")
            return
    except Exception:
        await message.answer("⚠️ Ошибка в датах. Попробуйте снова в формате: 01.01.2025 - 10.01.2025")
        return

    data = await state.get_data()
    base = data.get("base_answers", {})
    base["timing"] = {
        "start": start_date.strftime("%d.%m.%Y"),
        "end": end_date.strftime("%d.%m.%Y")
    }
    await state.update_data(base_answers=base)

    await message.answer("💰 Укажите бюджет (только число, в рублях):")
    await state.set_state(OrderStates.Base_Budget)


@router.message(OrderStates.Base_Budget)
async def base_budget(message: Message, state: FSMContext):
    text = message.text.strip().replace(" ", "")
    if not text.isdigit():
        await message.answer("⚠️ Укажите бюджет числом. Пример: 50000")
        return

    budget = int(text)
    if budget <= 0:
        await message.answer("⚠️ Бюджет должен быть положительным числом.")
        return

    data = await state.get_data()
    base = data.get("base_answers", {})
    base["budget"] = budget
    await state.update_data(base_answers=base)

    await go_to_next_service_block(message, state)
