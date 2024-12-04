from aiogram import types
from aiogram.fsm.context import FSMContext

from utils.settings import load_settings, save_settings
from utils import keyboards
from states import SetLastMessages
from .settings import settings_message_handler

async def set_last_messages(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработка кнопки для настройки последнего количества сообщений для реакции.
    """
    
    await callback_query.message.edit_text(
        "Введите количество последних сообщений, на которые бот должен реагировать (например, 5).",
        reply_markup=keyboards.cancel_button,
    )
    await state.set_state(SetLastMessages.waiting_for_messages_amount)

async def process_last_messages_count(message: types.Message, state: FSMContext):
    """
    Обработка введенного пользователем количества сообщений для реакции.
    """
    count = message.text.strip()

    if not count.isdigit():
        await message.answer("Пожалуйста, введите корректное число.")
        return

    count = int(count)

    settings = load_settings()

    settings["reactions"]["last_messages_count"] = count

    save_settings(settings)

    await message.answer(
        f"Количество последних сообщений для реакции успешно установлено: {count}.",
    )
    await settings_message_handler(message)
    await state.clear() 
