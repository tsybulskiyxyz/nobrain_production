from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from nobrain_bot.features.order.states import OrderStates
from nobrain_bot.features.order.utils import go_to_next_service_block


router = Router(name="order_site")


@router.message(OrderStates.Site_Idea)
async def site_idea(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("site", {})["idea"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "📦 Какие разделы вы хотите видеть на сайте?\n\n"
        "Например: «О компании», «Услуги», «Отзывы», «Контакты»"
    )
    await state.set_state(OrderStates.Site_Blocks)


@router.message(OrderStates.Site_Blocks)
async def site_blocks(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("site", {})["blocks"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "⚙️ Какие действия должен уметь выполнять сайт?\n\n"
        "Например: отправить заявку через форму, записаться онлайн, открыть карту, написать в WhatsApp/Telegram"
    )
    await state.set_state(OrderStates.Site_Functionality)


@router.message(OrderStates.Site_Functionality)
async def site_functionality(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("site", {})["functionality"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer("📑 У вас уже есть готовые тексты и фотографии для сайта или нужно будет подготовить всё с нуля?")
    await state.set_state(OrderStates.Site_Content)


@router.message(OrderStates.Site_Content)
async def site_content(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("site", {})["content"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "🎨 В каком стиле вы хотите сайт?\n\n"
        "Например: минимализм, современный, строгий, яркий, «люкс» и т.д."
    )
    await state.set_state(OrderStates.Site_Style)


@router.message(OrderStates.Site_Style)
async def site_style(message: Message, state: FSMContext):
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("site", {})["style"] = (message.text or "").strip()
    await state.update_data(details=details)

    await message.answer(
        "🔗 Есть ли референсы? Пришлите ссылки или файлы.\n\n"
        "Если нет — напишите «нет»."
    )
    await state.set_state(OrderStates.Site_Refs)


@router.message(OrderStates.Site_Refs)
async def site_refs(message: Message, state: FSMContext):
    # сохраняем референсы и закрываем ветку
    data = await state.get_data()
    details = data.get("details", {})
    details.setdefault("site", {})["refs"] = (message.text or "").strip()

    completed = set(data.get("completed_blocks", set()))
    completed.add("site")

    await state.update_data(details=details, completed_blocks=completed)
    await go_to_next_service_block(message, state)
