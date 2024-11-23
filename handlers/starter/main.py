from aiogram import types

async def handle_start_software(callback_query: types.CallbackQuery):
    """
    Обработка нажатия кнопки 'Запустить софт'
    """
    await callback_query.answer()
    await callback_query.message.answer("Запуск софта...")