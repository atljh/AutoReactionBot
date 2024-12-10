from copy import deepcopy

from aiogram import types
from aiogram.types import InlineKeyboardButton

import utils.keyboards as keyboards
from utils.config import load_config

async def list_admin(callback_query: types.CallbackQuery):
    config = load_config()
    admins = config.get('admins')

    if not admins:
        await callback_query.message.edit_text(
            "❌ <b>Список аккаунтов пуст.</b>",
            reply_markup=keyboards.admin_button,
            parse_mode="HTML"
        )
        return
    
    admins_list = []
    keyboard = deepcopy(keyboards.admin_button)
    for admin in admins:
        account_text = (
            f"👤 <b>{admin}</b>\n"
            f"———————————————"
        )
        admins_list.append(account_text)
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 Удалить {admin}",
                callback_data=f"delete_admin_{admin}",
            )
        ])
    message = "\n".join(admins_list)
    await callback_query.message.edit_text(
        message, reply_markup=keyboard, parse_mode="HTML"
    )

async def list_admin_message(message: types.Message):
    config = load_config()
    admins = config.get('admins')

    if not admins:
        await message.edit_text(
            "❌ <b>Список аккаунтов пуст.</b>",
            reply_markup=keyboards.admin_button,
            parse_mode="HTML"
        )
        return
    
    admins_list = []
    keyboard = deepcopy(keyboards.admin_button)
    for admin in admins:
        account_text = (
            f"👤 <b>{admin}</b>\n"
            f"———————————————"
        )
        admins_list.append(account_text)
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 Удалить {admin}",
                callback_data=f"delete_admin_{admin}",
            )
        ])
    message_text = "\n".join(admins_list)
    await message.answer(
        message_text, reply_markup=keyboard, parse_mode="HTML"
    )

