from aiogram import Dispatcher, types
from aiogram.filters import Command
import utils.keyboards as keyboards

async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для управления аккаунтами и реакциями. Выберите действие:",
        reply_markup=keyboards.start_menu
    )

def register_start_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
