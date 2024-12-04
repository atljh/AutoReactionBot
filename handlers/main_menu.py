from aiogram import Router, types, F
from aiogram.filters import Command

import utils.keyboards as keyboards
from utils.admin import user_is_admin

router = Router()

@router.callback_query(F.data == 'main_menu')
async def main_menu(callback_query: types.CallbackQuery):
    if not (await user_is_admin(
        user_id=callback_query.from_user.id,
        username=callback_query.from_user.username
    )):
        return
    await callback_query.message.edit_text(
        "Привет! Я бот для управления аккаунтами и реакциями. Выберите действие:",
        reply_markup=keyboards.main_menu
    )


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if not (await user_is_admin(user_id=message.from_user.id, username=message.from_user.username)):
        await message.answer("У вас нет прав для использования этого бота.")
        return

    await message.answer(
        "Привет! Я бот для управления аккаунтами и реакциями. Выберите действие:",
        reply_markup=keyboards.main_menu
    )


