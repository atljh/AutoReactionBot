from aiogram import types

from utils.admin import delete_admin_from_config
from .list_admin import list_admin

async def delete_admin_handler(callback_query: types.CallbackQuery):
    admin = callback_query.data.split("_")[-1]
    print(admin)
    if delete_admin_from_config(admin):
        await callback_query.answer(f"Админ {admin} удалён.")
    else:
        await callback_query.answer(f"Админ {admin} не найден.")

    await list_admin(callback_query)
