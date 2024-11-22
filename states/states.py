from aiogram.fsm.state import State, StatesGroup


class AddGroupStates(StatesGroup):
    waiting_for_group = State()

class AddAccountStates(StatesGroup):
    waiting_for_phone = State()

