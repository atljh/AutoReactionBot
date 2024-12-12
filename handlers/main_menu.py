import psutil

from aiogram import Router, types, F
from aiogram.filters import Command

import utils.keyboards as keyboards
from utils.admin import user_is_admin

router = Router()

def is_userbot_process_running():
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if process.info['cmdline'] and "python" in process.info['name'] and "-m" in process.info['cmdline'] and "userbot.main" in process.info['cmdline']:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

@router.callback_query(F.data == 'main_menu')
async def main_menu(callback_query: types.CallbackQuery):
    if not (await user_is_admin(
        user_id=callback_query.from_user.id,
        username=callback_query.from_user.username
    )):
        return
    userbot_running = is_userbot_process_running()
    status_emoji = "🟢" if userbot_running else "🔴"
    status_text = "активен" if userbot_running else "не активен"

    await callback_query.message.edit_text(
        f"👋 *Привет!*\n\n"
        f"Я бот для управления аккаунтами и реакциями.\n\n"
        f"🖥️ *Статус софта:* {status_emoji} {status_text}\n\n"
        f"📋 *Выберите действие:*",
        reply_markup=keyboards.main_menu,
        parse_mode="Markdown"
    )


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if not (await user_is_admin(user_id=message.from_user.id, username=message.from_user.username)):
        await message.answer("У вас нет прав для использования этого бота.")
        return

    userbot_running = is_userbot_process_running()
    status_emoji = "🟢" if userbot_running else "🔴"
    status_text = "активен" if userbot_running else "не активен"

    await message.answer(
        f"👋 *Привет!*\n\n"
        f"Я бот для управления аккаунтами и реакциями.\n\n"
        f"🖥️ *Статус софта:* {status_emoji} {status_text}\n\n"
        f"📋 *Выберите действие:*",
        reply_markup=keyboards.main_menu,
        parse_mode="Markdown"
    )

