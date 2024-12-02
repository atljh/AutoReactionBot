from aiogram import Dispatcher, types

import utils.keyboards as keyboards
from utils.users import user_is_admin

async def main_menu(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    if not (await user_is_admin(callback_query.from_user.id)):
        return
    await callback_query.message.answer(
        "Привет! Я бот для управления аккаунтами и реакциями. Выберите действие:",
        reply_markup=keyboards.main_menu
    )

def register_main_menu_handlers(dp: Dispatcher):
    dp.callback_query.register(main_menu, lambda c: c.data == "main_menu")
