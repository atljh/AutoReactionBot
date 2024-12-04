from aiogram import Router, F
from aiogram.fsm.state import State

from states import AddGroupStates
from .add_group import save_group_name, add_group_handler
from .delete_group import delete_group_handler
from .view_group import view_groups_handler

router = Router()


router.callback_query.register(view_groups_handler, F.data == "view_groups")

router.message.register(save_group_name, AddGroupStates.waiting_for_group)
router.callback_query.register(add_group_handler, F.data == "add_group")

router.callback_query.register(delete_group_handler, F.data.startswith("delete_group_"))
