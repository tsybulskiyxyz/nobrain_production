from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def about_kb(config) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="🌐 Перейти на сайт", url=config.site_url)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def blog_kb(config) -> InlineKeyboardMarkup:
    kb = [
          [InlineKeyboardButton(text="📖 Открыть блог", url=config.blog_url)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def manager_kb(config) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="📱 Написать менеджеру", url=config.manager_url)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
