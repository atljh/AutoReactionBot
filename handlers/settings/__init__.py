from aiogram import Router, F

from states import (
    WorkIntervalStates, IgnoreMessagesStates, SetLastMessages,
    SetEmojiState, SendDelay, AddAdminState, AddProxyState
)

from handlers.settings.settings import settings_handler
from handlers.settings.admin_bypass import toggle_admin_bypass_handler
from handlers.settings.work_interval import set_work_interval_handler, set_active_minutes, set_pause_minutes
from handlers.settings.ignore_messages import set_ignore_messages_handler, set_max_messages, set_min_messages
from handlers.settings.restart import restart_bot
from handlers.settings.set_last_messages import set_last_messages, process_last_messages_count
from handlers.settings.emoji import set_emoji, process_emoji_input, toggle_random_emojis_handler, clear_emojis
from handlers.settings.message_delay import set_delay_messages, process_delay_messages_count
from handlers.settings.admin import list_admin, add_admin_handler, admin_input_handler, delete_admin_handler
from handlers.settings.proxy import view_proxy_handler, add_proxy_handler, proxy_input_handler, delete_proxy_handler
router = Router()

router.callback_query(F.data == "settings")(settings_handler)
router.callback_query(F.data == "toggle_random_emojis")(toggle_random_emojis_handler)
router.callback_query(F.data == "toggle_admin_bypass")(toggle_admin_bypass_handler)
router.callback_query(F.data == "set_emoji")(set_emoji)
router.callback_query(F.data == "emoji_clear")(clear_emojis)
router.callback_query(F.data == "set_work_interval")(set_work_interval_handler)
router.callback_query(F.data == "set_ignore_messages")(set_ignore_messages_handler)
router.callback_query(F.data == "set_last_messages")(set_last_messages)
router.callback_query(F.data == "send_delay")(set_delay_messages)
router.callback_query(F.data == "list_admin")(list_admin)
router.callback_query(F.data == "add_admin")(add_admin_handler)
router.callback_query(F.data.startswith("delete_admin_"))(delete_admin_handler)
router.callback_query(F.data == "view_proxy")(view_proxy_handler)
router.callback_query(F.data == "add_proxy")(add_proxy_handler)
router.callback_query(F.data.startswith("delete_proxy_"))(delete_proxy_handler)

router.callback_query(F.data == "restart_bot")(restart_bot)

router.message.register(process_emoji_input, SetEmojiState.waiting_for_emoji)
router.message.register(set_active_minutes, WorkIntervalStates.waiting_for_active_minutes)
router.message.register(set_pause_minutes, WorkIntervalStates.waiting_for_pause_minutes)
router.message.register(set_min_messages, IgnoreMessagesStates.waiting_for_min_messages)
router.message.register(set_max_messages, IgnoreMessagesStates.waiting_for_max_messages)
router.message.register(process_last_messages_count, SetLastMessages.waiting_for_messages_amount)
router.message.register(process_delay_messages_count, SendDelay.waiting_for_delay)
router.message.register(admin_input_handler, AddAdminState.waiting_for_admin)
router.message.register(proxy_input_handler, AddProxyState.waiting_for_proxy)


