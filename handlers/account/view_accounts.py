from aiogram import types
from services.account_manager import list_sessions, get_account_info
import utils.keyboards as keyboards

async def view_accounts(callback_query: types.CallbackQuery):
    """
    Просмотр списка добавленных аккаунтов.
    """
    await callback_query.message.delete()
    sessions = list_sessions()

    if not sessions:
        await callback_query.message.answer("Список аккаунтов пуст.", reply_markup=keyboards.main_menu)
        return

    message = "Добавленные аккаунты:\n"
    for phone in sessions:
        account_info = await get_account_info(phone)
        if account_info:
            message += (
                f"\n📱 Номер: {account_info['phone']}\n"
                f"👤 Имя: {account_info['first_name']} {account_info['last_name']}\n"
                f"🔗 Юзернейм: @{account_info['username']}\n"
            )
        else:
            message += f"\n❌ Не удалось получить данные для номера {phone}."

    await callback_query.message.answer(message, reply_markup=keyboards.main_menu)
