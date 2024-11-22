import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import setup_handlers
from services.logging import setup_logging
from utils.console import console

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env file")

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
        console.log(f"[red]Ошибка: {e}[/red]")

if __name__ == "__main__":
    main()
