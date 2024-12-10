from aiogram import Router, F

from states import AddGroupStates
from .add_group import save_group_name, add_group_handler
from .delete_group import delete_group_handler
from .view_group import view_groups_handler
from .link_group import link_account_handler, confirm_link_handler, unlink_account_handler
from .set_active_group import activate_group_handler, delete_active_group_handler

router = Router()


router.callback_query.register(view_groups_handler, F.data == "view_groups")
router.callback_query.register(link_account_handler, F.data.startswith("link_account"))
router.callback_query.register(confirm_link_handler, F.data.startswith("confirm_link"))
router.callback_query.register(unlink_account_handler, F.data.startswith("unlink_account"))

router.callback_query.register(delete_active_group_handler, F.data.startswith("delete_active_group"))
router.callback_query.register(activate_group_handler, F.data.startswith("activate_group"))


router.message.register(save_group_name, AddGroupStates.waiting_for_group)
router.callback_query.register(add_group_handler, F.data == "add_group")
router.callback_query.register(delete_group_handler, F.data.startswith("delete_group_"))
