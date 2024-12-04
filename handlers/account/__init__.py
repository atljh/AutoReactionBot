from aiogram import Router, F
from handlers.account.add_account import (
    add_account_handler, process_phone_number, process_auth_code, process_password, AddAccountStates
)
from handlers.account.view_accounts import(
     view_accounts, handle_pagination, AccountsCallback, ToggleCallback, toggle_account_info_handler
)
from .delete_account import delete_account_handler

router = Router()

router.callback_query.register(handle_pagination, AccountsCallback.filter())
router.callback_query.register(view_accounts, F.data == "view_accounts")
router.callback_query.register(toggle_account_info_handler, ToggleCallback.filter())

router.callback_query.register(add_account_handler, F.data == 'add_account')
router.callback_query.register(delete_account_handler, F.data.startswith("delete_account_"))

router.message.register(process_phone_number, AddAccountStates.waiting_for_phone)
router.message.register(process_auth_code, AddAccountStates.waiting_for_code)
router.message.register(process_password, AddAccountStates.waiting_for_password)
