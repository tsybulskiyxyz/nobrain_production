from aiogram.utils.keyboard import InlineKeyboardBuilder

SERVICES = {
    "bot": "Бот",
    "logo": "Логотип",
    "site": "Сайт"
}


def services_kb(selected_services):
    kb = InlineKeyboardBuilder()
    for key, title in SERVICES.items():
        mark = "✅" if key in selected_services else "⬜"
        kb.button(text=f"{mark} {title}", callback_data=f"service:{key}")
    kb.button(text="➡️ Продолжить", callback_data="service:continue")
    kb.adjust(1)
    return kb.as_markup()
