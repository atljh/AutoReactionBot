import os

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils import keyboards 
from utils.settings import load_settings, save_settings
from utils.groups import list_groups

async def view_groups(callback_query: types.CallbackQuery):
    """
    Просмотр списка добавленных групп.
    """
    await callback_query.message.delete()
    groups = list_groups()
    
    if not groups:
        await callback_query.message.answer("❌ Список групп пуст.", reply_markup=keyboards.add_group_button)
        return
    
    message = "Добавленные группы:\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for group in groups:
        message += f"📛 <b>{group}</b>\n"
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 Удалить {group}",
                callback_data=f"delete_group_{group}",
            )
        ])
    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text="➕ Добавить группу", callback_data="add_group"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="settings")
        ]
    )
    await callback_query.message.answer(message, reply_markup=keyboard, parse_mode="HTML")

async def view_groups_message(message: types.Message):
    await message.delete()
    groups = list_groups()

    if not groups:
        await message.answer("❌ Список групп пуст.", reply_markup=keyboards.add_group_button)
        return
    
    message_text = "Добавленные группы:\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for group in groups:
        message_text += f"📛 <b>{group}</b>\n"
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 Удалить {group}",
                callback_data=f"delete_group_{group}",
            )
        ])
    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text="➕ Добавить группу", callback_data="add_group"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="settings")
        ]
    )
    await message.answer(message_text, reply_markup=keyboard, parse_mode="HTML")
