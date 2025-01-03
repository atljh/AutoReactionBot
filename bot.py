import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from handlers import router as main_router
from services.logging import setup_logging
from utils.console import console
from utils.config import load_config

config = load_config()

BOT_TOKEN = config.get("bot_token")
if not BOT_TOKEN:
    raise ValueError("bot_token is not set in config.json file")


async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    setup_logging()
    dp.include_router(main_router)
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    try:
        console.log("Бот запущен", style="green")
        await dp.start_polling(bot)
    except Exception as e:
        console.log(f"Ошибка: {e}", style="bold red")

if __name__ == "__main__":
    asyncio.run(main())
