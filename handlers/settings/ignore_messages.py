from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.settings import load_settings, save_settings
from utils.keyboards import settings_menu
from states import IgnoreMessagesStates

from .settings import settings_message_handler


async def set_ignore_messages_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Введите минимальное количество сообщений для пропуска (например, 1):",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(IgnoreMessagesStates.waiting_for_min_messages)

async def set_min_messages(message: types.Message, state: FSMContext):
    try:
        min_messages = int(message.text.strip())
        if min_messages < 0:
            raise ValueError

        await state.update_data(min_messages=min_messages)
        await message.answer(
            "Введите максимальное количество сообщений для пропуска (например, 5):"
        )
        await state.set_state(IgnoreMessagesStates.waiting_for_max_messages)

    except ValueError:
        await message.answer("Пожалуйста, введите неотрицательное число.")

async def set_max_messages(message: types.Message, state: FSMContext):
    try:
        max_messages = int(message.text.strip())
        if max_messages < 0:
            raise ValueError

        data = await state.get_data()
        min_messages = data["min_messages"]

        if max_messages < min_messages:
            await message.answer(
                "Максимальное значение не может быть меньше минимального. Попробуйте снова."
            )
            return

        settings = load_settings()
        settings["reactions"]["ingore_messages"] = [min_messages, max_messages]
        save_settings(settings)

        await settings_message_handler(message)
        await state.clear()

    except ValueError:
        await message.answer("Пожалуйста, введите неотрицательное число.")
