from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils import keyboards 


async def settings_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Ваши настройки: ", reply_markup=keyboards.settings_menu)