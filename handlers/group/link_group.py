from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.settings import load_settings, save_settings
from services.account_manager import list_sessions
from utils.groups import link_account_to_group

async def link_account_handler(callback_query: types.CallbackQuery):
    group = callback_query.data.split('_')[-1]
    accounts = list_sessions() 
    settings = load_settings()
    linked_accounts = settings.get("groups", {}).get(group, [])

    message = f"Группа <b>{group}</b>\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    # Отображение привязанных аккаунтов
    if linked_accounts:
        message += "🔗 Привязанные аккаунты:\n"
        for account in linked_accounts:
            message += f" - {account}\n"
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"❌ Отвязать {account}",
                    callback_data=f"unlink_account_{group}_{account}",
                )
            ])
    else:
        message += "❌ Пока нет привязанных аккаунтов.\n"

    available_accounts = [acc for acc in accounts if acc not in linked_accounts]
    if available_accounts:
        message += "\nВыберите аккаунт для привязки:"
        for account in available_accounts:
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"🔗 Привязать {account}",
                    callback_data=f"confirm_link_{group}_{account}",
                )
            ])
    else:
        message += "\n✅ Все доступные аккаунты уже привязаны."

    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="view_groups")
        ]
    )

    # Обновление сообщения с новой информацией
    await callback_query.message.edit_text(
        message,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def confirm_link_handler(callback_query: types.CallbackQuery):
    _, _, group, account = callback_query.data.split('_')
    success = link_account_to_group(group, account)

    # Создаем клавиатуру с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="view_groups")
        ]
    ])

    # Сообщение после привязки
    if success:
        await callback_query.answer(
            f"✅ Аккаунт <b>{account}</b> успешно привязан к группе <b>{group}</b>.",
            parse_mode="HTML"
        )
    else:
        await callback_query.answer(
            f"❌ Не удалось привязать аккаунт <b>{account}</b> к группе <b>{group}</b>.",
            parse_mode="HTML"
        )
    
    # После привязки возвращаем актуальную информацию о группе
    await link_account_handler(callback_query)

async def unlink_account_handler(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    group = data[-2]
    account = data[-1]

    settings = load_settings()

    # Удаление аккаунта из группы
    if group in settings.get("groups", {}) and account in settings["groups"][group]:
        settings["groups"][group].remove(account)
        save_settings(settings)
        await callback_query.answer(f"Аккаунт {account} отвязан от группы {group}.", show_alert=True)
    else:
        await callback_query.answer(f"Ошибка: Аккаунт {account} не найден в группе {group}.", show_alert=True)

    # После отвязки возвращаем актуальную информацию о группе
    await link_account_handler(callback_query)
