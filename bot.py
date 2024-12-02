import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import setup_handlers
from services.logging import setup_logging
from utils.console import console
from utils.config import load_config

config = load_config()

BOT_TOKEN = config.get("bot_token")
if not BOT_TOKEN:
    raise ValueError("bot_token is not set in config.json file")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

def main():
    setup_logging()
    setup_handlers(dp)    
    try:
        console.log("[green]Бот запущен[/green]")
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        console.log(f"Ошибка: {e}", style="bold red")

if __name__ == "__main__":
    main()
