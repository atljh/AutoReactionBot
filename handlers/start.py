from aiogram import Dispatcher, types
from aiogram.filters import Command

import utils.keyboards as keyboards
from utils.admin import user_is_admin

async def cmd_start(message: types.Message):
    await message.delete()
    if not (await user_is_admin(user_id=message.from_user.id, username=message.from_user.username)):
        return
    await message.answer(
        "Привет! Я бот для управления аккаунтами и реакциями. Выберите действие:",
        reply_markup=keyboards.main_menu
    )

def register_start_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
