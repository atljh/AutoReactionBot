from aiogram import Dispatcher, types
from handlers.starter.main import handle_start_software  

def register_starter_handlers(dp: Dispatcher):
    dp.callback_query.register(handle_start_software, lambda c: c.data == "start_software")