from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.account_manager import list_sessions, get_account_info
import utils.keyboards as keyboards


async def view_accounts(callback_query: types.CallbackQuery):
    """
    Просмотр списка добавленных аккаунтов.
    """
    await callback_query.message.delete()
    sessions = list_sessions()

    if not sessions:
        await callback_query.message.answer(
            "❌ <b>Список аккаунтов пуст.</b>",
            reply_markup=keyboards.main_menu,
            parse_mode="HTML"
        )
        return

    accounts = []
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for phone in sessions:
        account_info = await get_account_info(phone)
        if account_info:
            account_text = (
                f"📱 <b>Номер:</b> {account_info['phone']}\n"
                f"👤 <b>Имя:</b> {account_info['first_name']} {account_info['last_name']}\n"
                f"🔗 <b>Юзернейм:</b> @{account_info['username'] or '—'}\n"
                f"———————————————"
            )
            accounts.append(account_text)
        else:
            accounts.append(
                f"❌ <b>Не удалось получить данные для номера:</b> {phone}\n"
                f"———————————————"
            )
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 Удалить {phone}",
                callback_data=f"delete_account_{phone}",
            )
        ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="main_menu"
        )
    ])
    
    message = "\n\n".join(accounts)
    await callback_query.message.answer(
        message, reply_markup=keyboard, parse_mode="HTML"
    )
