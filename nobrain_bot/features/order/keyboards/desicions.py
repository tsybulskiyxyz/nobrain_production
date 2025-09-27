from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_confirm_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="✅ Принять", callback_data=f"accept:{order_id}"),
            InlineKeyboardButton(text="✏️ Внести изменения", callback_data=f"edit:{order_id}"),
            InlineKeyboardButton(text="❌ Отказать", callback_data=f"decline:{order_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def client_confirm_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="✅ Согласен", callback_data=f"client_accept:{order_id}"),
            InlineKeyboardButton(text="✏️ Предложить свои условия", callback_data=f"client_edit:{order_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)