from aiogram import types

from utils.proxy import delete_proxy
from .view_proxy import view_proxy_handler

async def delete_proxy_handler(callback_query: types.CallbackQuery):
    proxy = callback_query.data.split("_")[-1]

    if delete_proxy(proxy):
        await callback_query.answer(f"Прокси {proxy} удалён.")
    else:
        await callback_query.answer(f"Прокси {proxy} не найден.")

    await view_proxy_handler(callback_query)
