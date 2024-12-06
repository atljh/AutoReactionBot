from copy import deepcopy
from aiogram import types
from aiogram.types import InlineKeyboardButton

import utils.keyboards as keyboards
from utils.settings import load_settings

async def view_proxy_handler(callback_query: types.CallbackQuery):
    settings = load_settings()
    proxies = settings.get('proxy')

    if not proxies:
        await callback_query.message.edit_text(
            "❌ <b>Список прокси пуст.</b>",
            reply_markup=keyboards.proxy_button,
            parse_mode="HTML"
        )
        return
    
    proxy_list = []
    keyboard = deepcopy(keyboards.proxy_button)
    for proxy in proxies:
        proxy_text = (
            f"👤 <b>{proxy}</b>\n"
            f"———————————————"
        )
        proxy_list.append(proxy_text)
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 Удалить {proxy}",
                callback_data=f"delete_proxy_{proxy}",
            )
        ])
    message = "\n".join(proxy_list)
    await callback_query.message.edit_text(
        message, reply_markup=keyboard, parse_mode="HTML"
    )


async def view_proxy_handler_message(message: types.Message):
    settings = load_settings()
    proxies = settings.get('proxy')

    if not proxies:
        await message.edit_text(
            "❌ <b>Список прокси пуст.</b>",
            reply_markup=keyboards.proxy_button,
            parse_mode="HTML"
        )
        return
    
    proxy_list = []
    keyboard = deepcopy(keyboards.proxy_button)
    for proxy in proxies:
        proxy_text = (
            f"👤 <b>{proxy}</b>\n"
            f"———————————————"
        )
        proxy_list.append(proxy_text)
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"🗑 Удалить {proxy}",
                callback_data=f"delete_proxy_{proxy}",
            )
        ])
    message_text = "\n".join(proxy_list)
    await message.answer(
        message_text, reply_markup=keyboard, parse_mode="HTML"
    )

