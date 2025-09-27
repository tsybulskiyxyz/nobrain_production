from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from nobrain_bot.features.order.states import OrderStates
from nobrain_bot.features.order.keyboards.services import services_kb


router = Router(name="order_start")


@router.message(F.text == '📝 Оформить заказ')
async def start_order(message: Message, state: FSMContext):
    # очищаем прошлое состояние и готовим структуру
    await state.clear()
    await state.update_data(
        selected_services=set(),
        base_answers={},
        details={},
        completed_blocks=set()
    )
    await message.answer(
        "📝 Давайте сформируем заявку.\n\nВыберите одну или несколько услуг:",
        reply_markup=services_kb(set())
    )
    await state.set_state(OrderStates.ChoosingServices)


@router.callback_query(F.data.startswith("service:"), OrderStates.ChoosingServices)
async def choose_services(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(data.get("selected_services", set()))
    _, payload = callback.data.split(":", 1)

    if payload == "continue":
        if not selected:
            await callback.answer("Выберите хотя бы одну услугу", show_alert=True)
            return
        await callback.message.edit_text("💼 Расскажите вкратце о вашем бизнесе:")
        await state.set_state(OrderStates.Base_About)
        return

    if payload in selected:
        selected.remove(payload)
    else:
        selected.add(payload)
    await state.update_data(selected_services=selected)
    await callback.message.edit_reply_markup(reply_markup=services_kb(selected))
    await callback.answer()
