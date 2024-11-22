from aiogram import Dispatcher, types
from handlers.account.add_account import add_account, process_phone_number
from handlers.account.add_account import AddAccountStates
from handlers.account.view_accounts import view_accounts
from handlers.account.delete_account import delete_account

def register_account_handlers(dp: Dispatcher):
    dp.callback_query.register(delete_account, lambda c: c.data.startswith("delete_account_"))
    dp.callback_query.register(add_account, lambda c: c.data == "add_account")
    dp.message.register(process_phone_number, AddAccountStates.waiting_for_phone)
    dp.callback_query.register(view_accounts, lambda c: c.data == "view_accounts")
