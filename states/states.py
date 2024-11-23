from aiogram.fsm.state import State, StatesGroup

class AddAccountStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()
    waiting_for_password = State()

class AddGroupStates(StatesGroup):
    waiting_for_group = State()

class WorkIntervalStates(StatesGroup):
    waiting_for_active_minutes = State()
    waiting_for_pause_minutes = State()

class IgnoreMessagesStates(StatesGroup):
    waiting_for_min_messages = State()
    waiting_for_max_messages = State()

class SetLastMessages(StatesGroup):
    waiting_for_messages_amount = State()

class SetEmojiState(StatesGroup):
    waiting_for_emoji = State()