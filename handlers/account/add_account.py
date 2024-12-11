import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from telethon import TelegramClient, errors

from states import AddAccountStates
from utils.keyboards import cancel_button
from utils.config import load_config

config = load_config()
API_ID = config.get("api_id")
API_HASH = config.get("api_hash")



SESSION_FOLDER = "sessions"
os.makedirs(SESSION_FOLDER, exist_ok=True)


async def add_account_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Отправьте номер телефона в формате +1234567890",
        reply_markup=cancel_button,
    )
    await state.set_state(AddAccountStates.waiting_for_phone)


async def process_phone_number(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    if not phone.startswith("+"):
        await message.edit_text("Номер телефона должен начинаться с '+'. Попробуйте снова.")
        return

    try:
        session_path = os.path.join(SESSION_FOLDER, f"{phone}.session")
        client = TelegramClient(session_path, API_ID, API_HASH)

        await client.connect()
        result = await client.send_code_request(phone)

        await state.update_data(phone=phone, client=client)
        await message.answer(
            "Введите пришедший код уведомления добавив пробел после любой цифры\nНапример: 81 35",
            reply_markup=cancel_button,
        )
        await state.set_state(AddAccountStates.waiting_for_code)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}", reply_markup=cancel_button)
        await state.clear()


async def process_auth_code(message: types.Message, state: FSMContext):
    """
    Handle the confirmation code for login.
    """
    code = message.text.strip().replace(" ", '')
    data = await state.get_data()
    client: TelegramClient = data.get("client")

    try:
        # Use the existing client to complete the sign-in process
        await client.sign_in(code=code)
        user = await client.get_me()
        await message.answer(
            f"Аккаунт {user.first_name} успешно добавлен.", reply_markup=cancel_button
        )

        client.session.save()
        await client.disconnect()
        await state.clear()

    except errors.SessionPasswordNeededError:
        await message.answer("Введите ваш пароль для двухфакторной аутентификации.")
        await state.set_state(AddAccountStates.waiting_for_password)

    except Exception as e:
        await message.answer(f"Ошибка авторизации: {str(e)}. Попробуйте ещё раз.", reply_markup=cancel_button)


async def process_password(message: types.Message, state: FSMContext):
    """
    Handle the password for two-factor authentication.
    """
    password = message.text.strip()
    data = await state.get_data()
    client: TelegramClient = data.get("client")

    try:
        await client.sign_in(password=password)
        user = await client.get_me()
        await message.answer(
            f"Аккаунт {user.first_name} успешно добавлен.", reply_markup=cancel_button
        )

        client.session.save()
        await client.disconnect()
        await state.clear()

    except Exception as e:
        await message.answer(f"Ошибка авторизации: {str(e)}. Попробуйте ещё раз.", reply_markup=cancel_button)
