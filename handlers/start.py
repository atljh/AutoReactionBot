from aiogram import Dispatcher, types
from aiogram.filters import Command

import utils.keyboards as keyboards
from utils.users import user_is_admin

async def cmd_start(message: types.Message):
    await message.delete()
    if not (await user_is_admin(message.from_user.id)):
        return
    await message.answer(
        "Привет! Я бот для управления аккаунтами и реакциями. Выберите действие:",
        reply_markup=keyboards.main_menu
    )

def register_start_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
