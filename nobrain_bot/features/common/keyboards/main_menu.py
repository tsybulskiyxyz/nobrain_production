from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="🧠 Что такое nobrain_production?")],
        [KeyboardButton(text="📝 Оформить заказ")],
        [KeyboardButton(text="📱 Связаться с менеджером")],
        [ KeyboardButton(text="📰 Наш блог")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
