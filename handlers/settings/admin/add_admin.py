from aiogram import types
from aiogram.fsm.context import FSMContext

from states import AddAdminState

from utils.keyboards import back_settings_button
from .list_admin import list_admin_message
from utils.admin import add_admin_to_config

async def add_admin_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Отправьте id админа или его юзернейм",
        reply_markup=back_settings_button,
    )
    await state.set_state(AddAdminState.waiting_for_admin)

async def admin_input_handler(message: types.Message, state: FSMContext):
    admin = message.text.strip()

    add_admin_to_config(admin)

    await message.answer(
        "Админ успешно добавлен",
        reply_markup=back_settings_button,
    )
    await list_admin_message(message)
    await state.clear()

