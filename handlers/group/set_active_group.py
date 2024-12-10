from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.groups import set_active_group, delete_active_group
from .view_group import view_groups_handler

async def activate_group_handler(callback_query: types.CallbackQuery):
    group = callback_query.data.split('_')[-1]

    set_active_group(group)

    await callback_query.answer(
        f"Активная группа {group} установлена"
    )
    await view_groups_handler(callback_query)

async def delete_active_group_handler(callback_query: types.CallbackQuery):
    group = callback_query.data.split('_')[-1]

    delete_active_group(group)

    await callback_query.answer(
        f"Активная группа удалена"
    )
    await view_groups_handler(callback_query)