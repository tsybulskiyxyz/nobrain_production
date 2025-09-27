from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from nobrain_bot.features.order.states import OrderStates
from nobrain_bot.features.order.utils import go_to_next_service_block


router = Router(name="order_content")


@router.message(OrderStates.Content_Type)
async def content_type(message: Message, state: FSMContext):
    # сохраняем ОБЩЕЕ описание: что именно нужно по контенту
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("content", {})["type"] = (message.text or "").strip()
    await state.update_data(details=details)

    # следующий вопрос → площадка
    await message.answer(
        "📍 Для какой площадки нужен контент?\n\n"
        "Например: Telegram, Instagram, сайт, VK, YouTube"
    )
    await state.set_state(OrderStates.Content_Platform)


@router.message(OrderStates.Content_Platform)
async def content_platform(message: Message, state: FSMContext):
    # сохраняем площадку
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("content", {})["platform"] = (message.text or "").strip()
    await state.update_data(details=details)

    # следующий вопрос → стиль/подача
    await message.answer(
        "👩‍💻 В каком стиле или подаче должен быть контент?\n\n"
        "Например: дружелюбно, экспертно, дерзко, «люкс», сторителлинг и т.д."
    )
    await state.set_state(OrderStates.Content_Style)


@router.message(OrderStates.Content_Style)
async def content_style(message: Message, state: FSMContext):
    # сохраняем стиль/подачу
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("content", {})["style"] = (message.text or "").strip()
    await state.update_data(details=details)

    # следующий вопрос → референсы
    await message.answer(
        "🔗 Есть ли референсы или конкуренты, на чьи материалы стоит ориентироваться?\n\n"
        "Если нет — напишите «нет»."
    )
    await state.set_state(OrderStates.Content_Refs)


@router.message(OrderStates.Content_Refs)
async def content_refs(message: Message, state: FSMContext):
    # сохраняем референсы и закрываем ветку
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("content", {})["refs"] = (message.text or "").strip()

    completed = set(data.get("completed_blocks", set()))
    completed.add("content")

    await state.update_data(details=details, completed_blocks=completed)
    await go_to_next_service_block(message, state)
