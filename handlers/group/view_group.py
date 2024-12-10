from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils import keyboards 
from utils.groups import list_groups

async def view_groups_handler(callback_query: types.CallbackQuery):
    groups = list_groups()

    if not groups:
        await callback_query.message.edit_text(
            "❌ Список групп пуст.",
            reply_markup=keyboards.add_group_button
        )
        return

    message = "Добавленные группы:\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for group, accounts in groups.items():
        account_count = len(accounts)
        message += f"📛 <b>{group}</b> — Привязанных аккаунтов: <b>{account_count}</b>\n"

        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 Удалить {group}",
                callback_data=f"delete_group_{group}",
            ),
            InlineKeyboardButton(
                text=f"🔗 Привязать аккаунт",
                callback_data=f"link_account_{group}",
            )
        ])

    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text="➕ Добавить группу", callback_data="add_group"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="settings")
        ]
    )

    await callback_query.message.edit_text(
        message, reply_markup=keyboard,
        parse_mode="HTML"
    )


async def view_groups_message(message: types.Message):
    groups = list_groups()

    if not groups:
        await message.answer("❌ Список групп пуст.", reply_markup=keyboards.add_group_button)
        return

    message_text = "Добавленные группы:\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for group, accounts in groups.items():
        account_count = len(accounts)
        message_text += f"📛 <b>{group}</b> — Привязанных аккаунтов: <b>{account_count}</b>\n"

        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 Удалить {group}",
                callback_data=f"delete_group_{group}",
            ),
            InlineKeyboardButton(
                text=f"🔗 Привязать аккаунт",
                callback_data=f"link_account_{group}",
            )
        ])

    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text="➕ Добавить группу", callback_data="add_group"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="settings")
        ]
    )

    await message.answer(
        message_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
