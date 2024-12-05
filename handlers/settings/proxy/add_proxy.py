from aiogram import types
from aiogram.fsm.context import FSMContext

from states import AddProxyState

from utils.keyboards import back_settings_button
from .view_proxy import view_proxy_handler_message
from utils.proxy import add_proxy

async def add_proxy_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Отправьте прокси в формате: socks5:ipaddr:port:user:pswd",
        reply_markup=back_settings_button,
    )
    await state.set_state(AddProxyState.waiting_for_proxy)

async def proxy_input_handler(message: types.Message, state: FSMContext):
    proxy = message.text.strip()

    add_proxy(proxy)

    await message.answer(
        "Прокси успешно добавлен",
        reply_markup=back_settings_button,
    )
    await view_proxy_handler_message(message)
    await state.clear()

