from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import utils.keyboards as keyboards
from utils.config import load_config

async def list_admin(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    config = load_config()
    admins = config.get('admins')

    if not admins:
        await callback_query.message.answer(
            "❌ <b>Список аккаунтов пуст.</b>",
            reply_markup=keyboards.main_menu,
            parse_mode="HTML"
        )
        return
    
    admins_list = []
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text=f"➕ Добавить админа",
            callback_data=f"add_admin",
        )
    ])
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
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="settings"
        )
    ])
    message = "\n".join(admins_list)
    await callback_query.message.answer(
        message, reply_markup=keyboard, parse_mode="HTML"
    )


async def list_admin_message(message: types.Message):
    await message.delete()
    config = load_config()
    admins = config.get('admins')

    if not admins:
        await message.answer(
            "❌ <b>Список аккаунтов пуст.</b>",
            reply_markup=keyboards.main_menu,
            parse_mode="HTML"
        )
        return
    
    admins_list = []
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text=f"➕ Добавить админа",
            callback_data=f"add_admin",
        )
    ])
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
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="main_menu"
        )
    ])
    message_text = "\n".join(admins_list)
    await message.answer(
        message_text, reply_markup=keyboard, parse_mode="HTML"
    )


