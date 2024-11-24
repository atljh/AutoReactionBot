import os
import subprocess
from aiogram import types

telethon_process = None

async def handle_start_software(callback_query: types.CallbackQuery):
    """
    Обработка нажатия кнопки 'Запустить софт'
    """
    global telethon_process

    await callback_query.answer()

    if telethon_process is None:
        try:
            telethon_process = subprocess.Popen(["python", "reactions_bot.py"])
            await callback_query.message.answer("Telethon-бот успешно запущен!")
        except Exception as e:
            await callback_query.message.answer(f"Ошибка при запуске d-бота: {e}")
    else:
        await callback_query.message.answer("Telethon-бот уже работает.")

async def handle_stop_software(callback_query: types.CallbackQuery):
    """
    Обработка нажатия кнопки 'Остановить софт'
    """
    global telethon_process

    await callback_query.answer()

    if telethon_process is not None:
        try:
            telethon_process.terminate()
            telethon_process = None
            await callback_query.message.answer("Telethon-бот успешно остановлен.")
        except Exception as e:
            await callback_query.message.answer(f"Ошибка при остановке Telethon-бота: {e}")
    else:
        await callback_query.message.answer("Telethon-бот не был запущен.")