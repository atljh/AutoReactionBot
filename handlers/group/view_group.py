from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils import keyboards 
from utils.groups import list_groups, is_group_active

async def view_groups_handler(callback_query: types.CallbackQuery):
    groups = list_groups()

    if not groups:
        await callback_query.message.edit_text(
            "❌ <b>Список групп пуст.</b>",
            reply_markup=keyboards.add_group_button,
            parse_mode="HTML"
        )
        return

    message = "<b>📋 Список добавленных групп:</b>\n\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for group, accounts in groups.items():
        account_count = len(accounts)
        is_active = is_group_active(group)

        status = "🟢 <b>Активная</b>" if is_active else "🔴 <b>Неактивная</b>"
        message += f"📛 <b>{group}</b>\n"
        message += f"└ Привязанных аккаунтов: <b>{account_count}</b>\n"
        message += f"└ Статус: {status}\n\n"

        group_buttons = [
            InlineKeyboardButton(
                text=f"🗑 Удалить {group}",
                callback_data=f"delete_group_{group}",
            ),
            InlineKeyboardButton(
                text=f"🔗 Привязать аккаунт",
                callback_data=f"link_account_{group}",
            ),
        ]

        if is_active:
            group_buttons.append(
                InlineKeyboardButton(
                    text="⚪ Сделать неактивной",
                    callback_data=f"delete_active_group_{group}",
                )
            )
        else:
            group_buttons.append(
                InlineKeyboardButton(
                    text="🟢 Сделать активной",
                    callback_data=f"activate_group_{group}",
                )
            )

        keyboard.inline_keyboard.append(group_buttons)

    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text="➕ Добавить группу", callback_data="add_group"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="settings"),
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
