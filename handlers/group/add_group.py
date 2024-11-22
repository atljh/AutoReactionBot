import json

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.group.view_group import list_groups
from utils import keyboards

def add_group(group_name):
    groups = list_groups()
    groups.append(group_name)
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(groups, f, ensure_ascii=False, indent=4)

async def save_group_name(message: types.Message):
    group_name = message.text.strip()
    add_group(group_name)
    await message.answer(
        f"Группа <b>{group_name}</b> успешно добавлена!",
        reply_markup=keyboards.main_menu,
        parse_mode="HTML"
    )


async def add_group_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Введите название новой группы:",
        reply_markup=keyboards.back_button
    )
