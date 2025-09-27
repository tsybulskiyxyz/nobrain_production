from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from nobrain_bot.features.order.states import OrderStates
from nobrain_bot.features.order.utils import go_to_next_service_block

router = Router(name="order_bot")


@router.message(OrderStates.Bot_Type)
async def bot_type(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("bot", {})["type"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "⚙️ Для чего нужен бот? Что он должен помогать делать?\n\n"
        "Например: показывать каталог и оформлять заказы, вести запись, отвечать на вопросы, собирать заявки"
    )
    await state.set_state(OrderStates.Bot_Functionality)


@router.message(OrderStates.Bot_Functionality)
async def bot_functionality(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("bot", {})["functionality"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "💳 Нужно ли, чтобы бот принимал онлайн-оплату?\n\n"
        "Если да — укажите желаемый способ: YooKassa, СБП и т.д.)."
    )
    await state.set_state(OrderStates.Bot_Payment)


@router.message(OrderStates.Bot_Payment)
async def bot_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("bot", {})["payment"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "📩 Куда должны приходить заявки или уведомления из бота?\n\n"
        "Например: только вам, в общий чат команды, разным людям в зависимости от задачи или вовсе без уведомлений"
    )
    await state.set_state(OrderStates.Bot_Notifications)


@router.message(OrderStates.Bot_Notifications)
async def bot_notifications(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("bot", {})["access"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "🔗 Нужны ли какие-то дополнительные интеграции с другими платформами?\n\n"
        "Google Sheets, Email, Google Calendar и т.д."
    )
    await state.set_state(OrderStates.Bot_Integrations)


@router.message(OrderStates.Bot_Integrations)
async def bot_integrations(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("bot", {})["integrations"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "📷 Есть ли примеры ботов, которые вам нравятся? Можно скинуть ссылки или описать своими словами.\n\n"
        'Если нет — напишите "нет".'
    )
    await state.set_state(OrderStates.Bot_Refs)


@router.message(OrderStates.Bot_Refs)
async def bot_refs(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("bot", {})["refs"] = (message.text or "").strip()

    completed = set(data.get("completed_blocks", set()))
    completed.add("bot")

    await state.update_data(details=details, completed_blocks=completed)
    await go_to_next_service_block(message, state)
