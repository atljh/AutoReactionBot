import os

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.group.view_group import view_groups

GROUPS_FILE = 'groups.txt'

def delete_group(group_name):
    if not os.path.exists(GROUPS_FILE):
        return False

    with open(GROUPS_FILE, 'r', encoding='utf-8') as f:
        groups = [line.strip() for line in f.readlines()]

    if group_name in groups:
        groups.remove(group_name)
        with open(GROUPS_FILE, 'w', encoding='utf-8') as f:
            f.writelines(group + '\n' for group in groups)
        return True
    return False


async def delete_group_handler(callback_query: types.CallbackQuery):
    group_name = callback_query.data.split("_", 2)[2] 
    success = delete_group(group_name)

    if success:
        await callback_query.answer(f"Группа {group_name} успешно удалена.")
    else:
        await callback_query.answer(f"Группа {group_name}не найдена.")

    await view_groups(callback_query)
