import json

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.group.view_group import list_groups, view_groups
from utils import keyboards

def delete_group(group_name):
    groups = list_groups()
    if group_name in groups:
        groups.remove(group_name)
        with open('groups.json', 'w', encoding='utf-8') as f:
            json.dump(groups, f, ensure_ascii=False, indent=4)

async def delete_group_handler(callback_query: types.CallbackQuery):
    """
    Удаление группы.
    """
    group_name = callback_query.data.split("_", 2)[2] 
    delete_group(group_name)
    await callback_query.answer(f"Группа <b>{group_name}</b> удалена.", parse_mode="HTML")
    await callback_query.message.delete()

    await view_groups(callback_query)
