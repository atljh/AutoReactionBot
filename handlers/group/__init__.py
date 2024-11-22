from aiogram import Dispatcher

from handlers.group.add_group import add_group_handler, save_group_name
from handlers.group.view_group import view_groups
from handlers.group.delete_group import delete_group_handler
from handlers.group.add_group import AddGroupStates

def register_group_handlers(dp: Dispatcher):
    dp.callback_query.register(delete_group_handler, lambda c: c.data.startswith("delete_group_"))
    dp.callback_query.register(view_groups, lambda c: c.data == "view_groups")
    dp.message.register(save_group_name, AddGroupStates.waiting_for_group)
    dp.callback_query.register(add_group_handler, lambda c: c.data == "add_group")
