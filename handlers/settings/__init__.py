from aiogram import Dispatcher, types
from handlers.settings.settings import settings_handler 
from handlers.settings.emoji import setup_reactions, toggle_random_emojis_handler
from services.emoji_service import process_emoji_selection

def register_settings_handlers(dp: Dispatcher):
    dp.callback_query.register(settings_handler, lambda c: c.data == "settings")
    dp.callback_query.register(setup_reactions, lambda c: c.data == "setup_reactions")
    dp.callback_query.register(toggle_random_emojis_handler, lambda c: c.data == "toggle_random_emojis")
    dp.callback_query.register(process_emoji_selection, lambda c: c.data.startswith("emoji_"))
