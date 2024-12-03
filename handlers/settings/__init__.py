from aiogram import Dispatcher

from handlers.settings.settings import settings_handler
from handlers.settings.admin_bypass import toggle_admin_bypass_handler
from handlers.settings.work_interval import set_work_interval_handler, set_active_minutes, set_pause_minutes
from handlers.settings.ignore_messages import set_ignore_messages_handler, set_max_messages, set_min_messages
from handlers.settings.restart import restart_bot
from handlers.settings.set_last_messages import set_last_messages, process_last_messages_count
from handlers.settings.emoji import set_emoji, process_emoji_input, toggle_random_emojis_handler, clear_emojis
from handlers.settings.message_delay import set_delay_messages, process_delay_messages_count
from handlers.settings.admin import list_admin, add_admin_handler, admin_input_handler, delete_admin_handler

from states import (
    WorkIntervalStates, IgnoreMessagesStates, SetLastMessages,
    SetEmojiState, SendDelay, AddAdminState
)


def register_settings_handlers(dp: Dispatcher):
    dp.callback_query.register(settings_handler, lambda c: c.data == "settings")
    dp.callback_query.register(toggle_random_emojis_handler, lambda c: c.data == "toggle_random_emojis")
    dp.callback_query.register(toggle_admin_bypass_handler, lambda c: c.data == "toggle_admin_bypass")

    dp.callback_query.register(set_emoji, lambda c: c.data == "set_emoji")
    dp.callback_query.register(clear_emojis, lambda c: c.data == "emoji_clear")
    dp.message.register(process_emoji_input, SetEmojiState.waiting_for_emoji)

    dp.callback_query.register(set_work_interval_handler, lambda c: c.data == "set_work_interval")
    dp.message.register(set_active_minutes, WorkIntervalStates.waiting_for_active_minutes)
    dp.message.register(set_pause_minutes, WorkIntervalStates.waiting_for_pause_minutes)

    dp.callback_query.register(set_ignore_messages_handler, lambda c: c.data == "set_ignore_messages")
    dp.message.register(set_min_messages, IgnoreMessagesStates.waiting_for_min_messages)
    dp.message.register(set_max_messages, IgnoreMessagesStates.waiting_for_max_messages)
    
    dp.callback_query.register(set_last_messages, lambda c: c.data == "set_last_messages")
    dp.message.register(process_last_messages_count, SetLastMessages.waiting_for_messages_amount)

    dp.callback_query.register(set_delay_messages, lambda c: c.data == "send_delay")
    dp.message.register(process_delay_messages_count, SendDelay.waiting_for_delay)

    dp.callback_query.register(list_admin, lambda c: c.data == "list_admin")
    dp.callback_query.register(add_admin_handler, lambda c: c.data == "add_admin")
    dp.callback_query.register(delete_admin_handler, lambda c: c.data.startswith("delete_admin_"))
    dp.message.register(admin_input_handler, AddAdminState.waiting_for_admin)

    dp.callback_query.register(restart_bot, lambda c: c.data == "restart_bot")
