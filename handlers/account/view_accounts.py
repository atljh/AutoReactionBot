from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import utils.keyboards as keyboards
from services.account_manager import list_sessions, get_account_info

class AccountsCallback(CallbackData, prefix="accounts"):
    action: str
    page: int

class ToggleCallback(CallbackData, prefix="toggle"):
    action: str

FETCH_ACCOUNT_INFO = False

async def handle_pagination(callback_query: types.CallbackQuery, callback_data: AccountsCallback):
    if callback_data.action == "view":
        await view_accounts(callback_query, page=callback_data.page)

async def toggle_account_info_handler(callback_query: types.CallbackQuery, callback_data: ToggleCallback):
    global FETCH_ACCOUNT_INFO
    FETCH_ACCOUNT_INFO = not FETCH_ACCOUNT_INFO
    await view_accounts(callback_query)

async def generate_accounts_menu(page: int = 1):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[], row_width=1)

    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(
            text="Переключить получение информации",
            callback_data=ToggleCallback(action="toggle_fetch").pack()
        )]
    )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(
            text="⬅️ В главное меню",
            callback_data="main_menu"
        )]
    )
    return keyboard

async def view_accounts(callback_query: types.CallbackQuery, page: int = 1):
    """
    Просмотр списка добавленных аккаунтов с пагинацией.
    """
    sessions = list_sessions()

    if not sessions:
        await callback_query.message.edit_text(
            "❌ <b>Список аккаунтов пуст.</b>",
            reply_markup=await generate_accounts_menu(),
            parse_mode="HTML"
        )
        return

    # Настройки пагинации
    items_per_page = 5
    total_sessions = len(sessions)
    total_pages = (total_sessions + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_sessions = sessions[start_index:end_index]

    accounts = []
    keyboard = InlineKeyboardMarkup(inline_keyboard=[], row_width=1)

    for phone in current_sessions:
        if FETCH_ACCOUNT_INFO:
            account_info = await get_account_info(phone)
            if account_info:
                accounts.append(
                    f"📱 <b>Номер:</b> {account_info['phone']}\n"
                    f"👤 <b>Имя:</b> {account_info['first_name']} {account_info['last_name']}\n"
                    f"🔗 <b>Юзернейм:</b> @{account_info['username'] or '—'}\n"
                    "———————————————"
                )
            else:
                accounts.append(
                    f"❌ <b>Не удалось получить данные для номера:</b> {phone}\n"
                    "———————————————"
                )
        else:
            accounts.append(
                f"📱 <b>Номер:</b> {phone}\n"
                "———————————————"
            )

        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(
                text=f"🗑 Удалить {phone}",
                callback_data=f"delete_account_{phone}",
            )]
        )

    if page > 1:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=AccountsCallback(action="view", page=page - 1).pack()
            )]
        )
    if page < total_pages:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(
                text="➡️ Вперед",
                callback_data=AccountsCallback(action="view", page=page + 1).pack()
            )]
        )

    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(
            text="⬅️ В главное меню",
            callback_data="main_menu"
        )]
    )
    if FETCH_ACCOUNT_INFO:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(
                text="Выключить получение информации",
                callback_data=ToggleCallback(action="toggle_fetch").pack()
            )]
        )
    else:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(
                text="Включить получение информации",
                callback_data=ToggleCallback(action="toggle_fetch").pack()
            )]
        )
    message = "\n".join(accounts)
    await callback_query.message.edit_text(
        message, reply_markup=keyboard, parse_mode="HTML"
    )
