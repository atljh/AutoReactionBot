import os
from aiogram import types
from handlers.account import view_accounts


async def delete_account(callback_query: types.CallbackQuery):
    """
    Удаляет указанный аккаунт.
    """
    phone = callback_query.data.split("_")[-1]
    session_path = os.path.join("sessions", f"{phone}.session")
    if os.path.exists(session_path):
        os.remove(session_path)
        await callback_query.answer(f"Аккаунт {phone} удалён.", show_alert=True)
    else:
        await callback_query.answer(f"Аккаунт {phone} не найден.", show_alert=True)

    await view_accounts(callback_query)
