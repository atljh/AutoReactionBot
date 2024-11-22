from aiogram import Dispatcher, types
import utils.keyboards as keyboards

async def add_account(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Отправьте номер телефона",
        reply_markup=keyboards.back_button
    )

async def show_accounts(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Список аккаунтов:",
        reply_markup=keyboards.back_button
    )

def register_account_handlers(dp: Dispatcher):
    dp.callback_query.register(add_account, lambda c: c.data == "add_account")
    dp.callback_query.register(show_accounts, lambda c: c.data == "show_accounts")
