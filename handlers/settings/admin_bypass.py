from aiogram import types
from aiogram.types import CallbackQuery

from utils import keyboards
from utils.groups import list_groups
from utils.settings import load_settings, save_settings
from .settings import settings_handler

async def toggle_admin_bypass_handler(callback_query: CallbackQuery):
    await toggle_admin_bypass(callback_query)

async def toggle_admin_bypass(callback_query: types.CallbackQuery):
    settings = load_settings()

    new_status = not settings["reactions"]["admin_bypass"]
    settings["reactions"]["admin_bypass"] = new_status

    save_settings(settings)
    
    await settings_handler(callback_query)
