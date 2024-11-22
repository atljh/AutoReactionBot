from aiogram.fsm.state import State, StatesGroup


class AddGroupStates(StatesGroup):
    waiting_for_group = State()

class AddAccountStates(StatesGroup):
    waiting_for_phone = State()

class WorkIntervalStates(StatesGroup):
    waiting_for_active_minutes = State()
    waiting_for_pause_minutes = State()
