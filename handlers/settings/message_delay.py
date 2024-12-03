from aiogram import types
from aiogram.fsm.context import FSMContext

from utils.settings import load_settings, save_settings
from utils import keyboards
from states import SendDelay

from .settings import settings_message_handler

async def set_delay_messages(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработка кнопки для настройки задержки между реакциями.
    """
    await callback_query.message.delete()
    
    await callback_query.message.answer(
        "Введите время в секундах для задержки между реакциями.",
        reply_markup=keyboards.back_settings_button,
    )
    await state.set_state(SendDelay.waiting_for_delay)


async def process_delay_messages_count(message: types.Message, state: FSMContext):
    """
    Обработка введенного пользователем задержки для реакции.
    """
    count = message.text.strip()

    if not count.isdigit():
        await message.answer("Пожалуйста, введите корректное число.")
        return

    delay = int(count)

    settings = load_settings()

    settings["reactions"]["send_delay"] = delay

    save_settings(settings)

    await message.answer(
        f"Задержка между реакциями успешно установлена: {count} сек.",
    )
    await settings_message_handler(message)
    await state.clear() 
