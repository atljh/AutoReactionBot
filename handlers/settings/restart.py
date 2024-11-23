import os
import sys
from aiogram import types

from utils.console import console

async def restart_bot(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Перезагрузка бота...\nОтправьте /start")
    
    console.log("Бот перезапускается...", style="yellow")

    os.execv(sys.executable, ['python'] + sys.argv)

