import asyncio
from aiogram import Bot, Dispatcher
from core.config import get_settings
from nobrain_bot.core.routers import setup_routers


async def main():
    config = get_settings()
    bot = Bot(token=config.bot_token)

    dp = Dispatcher()
    dp.include_router(setup_routers())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())