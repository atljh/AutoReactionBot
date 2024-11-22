from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from utils import keyboards 

def list_groups():
    try:
        with open('groups.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

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
        keyboard.add(
            InlineKeyboardButton(
                text=f"🗑 Удалить {group}",
                callback_data=f"delete_group_{group}",
            )
        )

    await callback_query.message.answer(message, reply_markup=keyboard, parse_mode="HTML")

