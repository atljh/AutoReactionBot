from aiogram import types
from aiogram.fsm.context import FSMContext

from states import WorkIntervalStates
from utils.settings import load_settings, save_settings
from .settings import settings_message_handler

async def set_work_interval_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Введите время работы в минутах (например, 10):",
    )
    await state.set_state(WorkIntervalStates.waiting_for_active_minutes)

async def set_active_minutes(message: types.Message, state: FSMContext):
    try:
        active_minutes = int(message.text.strip())
        if active_minutes <= 0:
            raise ValueError

        await state.update_data(active_minutes=active_minutes)
        await message.answer(
            "Введите время паузы в минутах (например, 20):",
        )
        await state.set_state(WorkIntervalStates.waiting_for_pause_minutes)

    except ValueError:
        await message.answer("Пожалуйста, введите положительное число минут.")

async def set_pause_minutes(message: types.Message, state: FSMContext):
    try:
        pause_minutes = int(message.text.strip())
        if pause_minutes <= 0:
            raise ValueError

        data = await state.get_data()
        active_minutes = data["active_minutes"]

        settings = load_settings()
        settings["reactions"]["work_intervals"]["active_minutes"] = active_minutes
        settings["reactions"]["work_intervals"]["pause_minutes"] = pause_minutes
        save_settings(settings)
        await state.clear()
        await settings_message_handler(message)

    except ValueError:
        await message.answer("Пожалуйста, введите положительное число минут.")
