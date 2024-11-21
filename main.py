import os
import logging
import asyncio
from dotenv import load_dotenv
from rich.console import Console
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

import keyboards

console = Console()

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set в .env file")

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

chosen_emojis = []

async def start(message: types.Message):
    keyboard = keyboards.start_menu
    await message.answer(
        "Привет! Я бот для управления аккаунтами и реакциями. Выберите действие:",
        reply_markup=keyboard
    )
    
async def main_menu(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(
        callback_query.from_user.id,
        text='Привет! Я бот для управления аккаунтами и реакциями. Выберите действие:',
        reply_markup=keyboards.start_menu
    )

async def choose_emojis(chat_id: int):
    keyboard = keyboards.choose_emojis
    await bot.send_message(
        chat_id,
        "Выберите эмодзи для реакций (можно выбрать несколько). Нажмите 'Завершить выбор', чтобы подтвердить:",
        reply_markup=keyboard
    )

async def add_account(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(
        callback_query.from_user.id,
        text='Отправьте номер телефона',
        reply_markup=keyboards.back_button
    )

async def process_emoji_selection(callback_query: types.CallbackQuery):
    global chosen_emojis

    emoji = callback_query.data.split("_")[1]

    if emoji == "done":
        await bot.answer_callback_query(callback_query.id)
        selected = ", ".join(chosen_emojis) if chosen_emojis else "Вы ничего не выбрали."
        await bot.send_message(callback_query.from_user.id, f"Выбранные эмодзи: {selected}")
        
        console.log(f"[green]Итоговый выбор эмодзи: {chosen_emojis}[/green]")
        chosen_emojis = []
    else:
        if emoji not in chosen_emojis:
            chosen_emojis.append(emoji)

        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f"Вы добавили эмодзи: {emoji}")

        console.log(f"[blue]Добавлено эмодзи: {emoji}[/blue]")

async def process_setup_reactions(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.answer_callback_query(callback_query.id)
    await choose_emojis(callback_query.from_user.id)

async def cmd_start(message: types.Message):
    await start(message)

dp.message.register(cmd_start, Command("start"))
dp.callback_query.register(main_menu, lambda c: c.data == "main_menu")
dp.callback_query.register(process_emoji_selection, lambda c: c.data.startswith("emoji_"))
dp.callback_query.register(process_setup_reactions, lambda c: c.data == "setup_reactions")
dp.callback_query.register(add_account, lambda c: c.data == "add_account")


async def main():
    try:
        console.log("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        console.log(f"[red]Ошибка при запуске бота: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())
