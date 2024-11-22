from aiogram import Dispatcher, types
from handlers.settings.settings import settings_handler 

def register_settings_handlers(dp: Dispatcher):
    dp.callback_query.register(settings_handler, lambda c: c.data == "settings")
