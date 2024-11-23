from aiogram import Dispatcher

from handlers.settings.settings import settings_handler
from handlers.settings.emoji import setup_reactions, process_emoji_selection, toggle_random_emojis_handler
from handlers.settings.admin_bypass import toggle_admin_bypass_handler
from handlers.settings.work_interval import set_work_interval_handler, set_active_minutes, set_pause_minutes
from handlers.settings.ignore_messages import set_ignore_messages_handler, set_max_messages, set_min_messages

from states import WorkIntervalStates, IgnoreMessagesStates

def register_settings_handlers(dp: Dispatcher):
    dp.callback_query.register(settings_handler, lambda c: c.data == "settings")
    dp.callback_query.register(setup_reactions, lambda c: c.data == "setup_reactions")
    dp.callback_query.register(toggle_random_emojis_handler, lambda c: c.data == "toggle_random_emojis")
    dp.callback_query.register(toggle_admin_bypass_handler, lambda c: c.data == "toggle_admin_bypass")
    dp.callback_query.register(process_emoji_selection, lambda c: c.data.startswith("emoji_"))

    dp.callback_query.register(set_work_interval_handler, lambda c: c.data == "set_work_interval")
    dp.message.register(set_active_minutes, WorkIntervalStates.waiting_for_active_minutes)
    dp.message.register(set_pause_minutes, WorkIntervalStates.waiting_for_pause_minutes)

    dp.callback_query.register(set_ignore_messages_handler, lambda c: c.data == "set_ignore_messages")
    dp.message.register(set_min_messages, IgnoreMessagesStates.waiting_for_min_messages)
    dp.message.register(set_max_messages, IgnoreMessagesStates.waiting_for_max_messages)