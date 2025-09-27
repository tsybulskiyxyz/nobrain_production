from nobrain_bot.features.order.states import OrderStates
from nobrain_bot.features.order.handlers.finalize_order import finalize_order


async def go_to_next_service_block(message, state):
    data = await state.get_data()
    selected = list(data.get("selected_services", []))
    completed = set(data.get("completed_blocks", set()))

    next_key = None
    for key in selected:
        if key not in completed:
            next_key = key
            break

    if next_key is None:
        await finalize_order(message, state, message.bot)
        return

    if next_key == "bot":
        await state.set_state(OrderStates.Bot_Type)
        await message.answer(
            "🤖 Перейдём к вопросам про Telegram-бота.\n"
            "Пожалуйста, дайте общее описание, какой тип бота нужен и какая у него основная задача:")
    elif next_key == "logo":
        await state.set_state(OrderStates.Logo_Idea)
        await message.answer(
            "🖌️ Обсудим логотип.\n"
            "Опишите, пожалуйста, общими словами, как вы представляете ваш логотип:")
    elif next_key == "site":
        await state.set_state(OrderStates.Site_Idea)
        await message.answer(
            "🌐 Сфокусируемся на сайте.\n"
            "Объясните в общих чертах, какая идея/замысел сайта:")
    elif next_key == "content":
        await state.set_state(OrderStates.Content_Type)
        await message.answer(
            "✍️ Поговорим про контент.\n"
            "Расскажите, пожалуйста, какой тип контента вам нужен и для чего:")
