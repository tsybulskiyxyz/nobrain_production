from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from nobrain_bot.features.order.states import OrderStates
from nobrain_bot.features.order.utils import go_to_next_service_block


router = Router(name="order_logo")


@router.message(OrderStates.Logo_Idea)
async def logo_idea(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("logo", {})["idea"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "🎨 В каком стиле вы хотите логотип?\n\n"
        "Например: минимализм, современный, люкс, игривый, рукописный и т.д."
    )
    await state.set_state(OrderStates.Logo_Style)


@router.message(OrderStates.Logo_Style)
async def logo_style(message: Message, state: FSMContext):
    # сохраняем стиль
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("logo", {})["style"] = (message.text or "").strip()
    await state.update_data(details=details)

    # следующий вопрос
    await message.answer(
        "🌈 Есть ли цвета, которые точно нужно использовать или наоборот лучше исключить?")
    await state.set_state(OrderStates.Logo_Colors)


@router.message(OrderStates.Logo_Colors)
async def logo_colors(message: Message, state: FSMContext):
    # сохраняем цвета
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("logo", {})["colors"] = (message.text or "").strip()
    await state.update_data(details=details)

    # следующий вопрос
    await message.answer(
        "🖨 Планируете ли вы использовать логотип в печати?\n\n"
        "Например: визитки, упаковка, баннеры, мерч"
    )
    await state.set_state(OrderStates.Logo_Print)


@router.message(OrderStates.Logo_Print)
async def logo_print(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("logo", {})["print"] = (message.text or "").strip()
    await state.update_data(details=details)

    # следующий вопрос → референсы
    await message.answer(
        "🔗 Есть ли референсы? Пришлите ссылки или файлы.\n\n"
        "Если нет — напишите «нет»."
    )
    await state.set_state(OrderStates.Logo_Refs)


@router.message(OrderStates.Logo_Refs)
async def logo_refs(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("logo", {})["refs"] = (message.text or "").strip()

    completed = set(data.get("completed_blocks", set()))
    completed.add("logo")

    await state.update_data(details=details, completed_blocks=completed)
    await go_to_next_service_block(message, state)
