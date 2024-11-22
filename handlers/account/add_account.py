import re

from aiogram import types
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import utils.keyboards as keyboards
from services.telethon_sessions import create_telethon_session

class AddAccountStates(StatesGroup):
    waiting_for_phone = State()


async def add_account(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Начало добавления аккаунта: запрос телефона.
    """
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Отправьте номер телефона в формате +1234567890",
        reply_markup=keyboards.cancel_button
    )
    await state.set_state(AddAccountStates.waiting_for_phone)


async def process_phone_number(message: types.Message, state: FSMContext):
    """
    Обработка отправленного номера телефона.
    """
    phone = message.text.strip()
    if not phone.startswith("+"):
        await message.answer(
            "Номер телефона должен начинаться с '+'. Попробуйте снова."
        )
        return

    try:
        await message.answer("Создаю сессию для аккаунта...")
        client = await create_telethon_session(phone)
        me = await client.get_me()

        await message.answer(
            f"Аккаунт {me.first_name} успешно добавлен.",
            reply_markup=keyboards.main_menu
        )
        await client.disconnect()
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Произошла ошибка: {str(e)}",
            reply_markup=keyboards.main_menu
        )
        await state.clear()


