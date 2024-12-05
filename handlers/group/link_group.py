from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.account_manager import list_sessions


async def link_account_handler(callback_query: types.CallbackQuery):
    await callback_query.answer("Выберите аккаунт для привязки к группе.")
    group_name = callback_query.data.split("_", 2)[2]
    accounts = list_sessions()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for account in accounts:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"Привязать к {account}",
                callback_data=f"confirm_link_{account}_{group_name}"
            )
        ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Назад", callback_data="view_groups"
        )
    ])
    await callback_query.message.edit_text(
        "Выберите аккаунт для привязки:",
        reply_markup=keyboard,
    )
