from aiogram import types

from handlers.group.view_group import view_groups_handler
from utils.groups import delete_group

async def delete_group_handler(callback_query: types.CallbackQuery):
    group_name = callback_query.data.split("_", 2)[2]
    success = delete_group(group_name)

    if success:
        await callback_query.answer(f"Группа {group_name} успешно удалена.")
    else:
        await callback_query.answer(f"Группа {group_name} не найдена.")

    await view_groups_handler(callback_query)
