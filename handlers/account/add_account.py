import asyncio
import os
import re
from dotenv import load_dotenv
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient, errors
from states import AddAccountStates

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_FOLDER = "sessions"
os.makedirs(SESSION_FOLDER, exist_ok=True)

cancel_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")],
])


async def add_account(callback_query: types.CallbackQuery, state: FSMContext):

    await callback_query.message.delete()
    await callback_query.message.answer(
        "Отправьте номер телефона в формате +1234567890",
        reply_markup=cancel_button,
    )
    await state.set_state(AddAccountStates.waiting_for_phone)


async def process_phone_number(message: types.Message, state: FSMContext):

    phone = message.text.strip()
    if not phone.startswith("+"):
        await message.answer("Номер телефона должен начинаться с '+'. Попробуйте снова.")
        return

    try:
        session_path = os.path.join(SESSION_FOLDER, f"{phone}.session")
        client = TelegramClient(session_path, API_ID, API_HASH)

        await client.connect()
        result = await client.send_code_request(phone)

        await state.update_data(phone=phone, client=client)
        await message.answer(
            "Код подтверждения отправлен. Введите его.",
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
    code = re.sub(r"\D", "", message.text.strip()) 
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
