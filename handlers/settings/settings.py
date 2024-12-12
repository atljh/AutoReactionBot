from aiogram import types, F

from utils import keyboards
from utils.settings import load_settings
from handlers.main_menu import is_userbot_process_running


async def settings_handler(callback_query: types.CallbackQuery):
    settings = load_settings()
    userbot_active = is_userbot_process_running()

    reactions = settings["reactions"]
    formatted_settings = (
        "<b>Ваши настройки:</b>\n\n"
        f"<b>Группы:</b> {len(settings['groups'])} групп\n\n"
        f"<b>Эмодзи для реакций:</b> {', '.join(reactions['emojis'])}\n"
        f"<b>Рандомные эмодзи:</b> {'<i>Включено</i>' if reactions['random_emojis'] else '<i>Выключено</i>'}\n\n"
        f"<b>Обход администраторов:</b> {'<i>Включено</i>' if reactions['admin_bypass'] else '<i>Выключено</i>'}\n\n"
        f"<b>Последних сообщений для реакции:</b> {reactions['last_messages_count']}\n"
        f"<b>Пропускать сообщения:</b> {reactions['ingore_messages'][0]} - {reactions['ingore_messages'][1]}\n\n"
        f"<b>Задержка между реакциями:</b> {reactions['send_delay']} сек\n\n"
        f"<b>Интервал работы:</b>\n"
        f"🕐 <i>{reactions['work_intervals']['active_minutes']}</i> минут работы\n"
        f"⏸️ <i>{reactions['work_intervals']['pause_minutes']}</i> минут паузы\n\n"
        f"<b>Telethon-бот:</b> {'<i>Запущен</i>' if userbot_active else '<i>Остановлен</i>'}\n\n"
        "<b>Вы можете обновить эти настройки в любой момент через меню!</b>\n"
    )

    await callback_query.message.edit_text(
        formatted_settings,
        reply_markup=keyboards.settings_menu,
        parse_mode="HTML"
    )


async def settings_message_handler(message: types.Message):
    settings = load_settings()
    userbot_active = is_userbot_process_running()

    reactions = settings["reactions"]
    formatted_settings = (
        "<b>Ваши настройки:</b>\n\n"
        f"<b>Группы:</b> {len(settings['groups'])} групп\n\n"
        f"<b>Эмодзи для реакций:</b> {', '.join(reactions['emojis'])}\n"
        f"<b>Рандомные эмодзи:</b> {'<i>Включено</i>' if reactions['random_emojis'] else '<i>Выключено</i>'}\n\n"
        f"<b>Обход администраторов:</b> {'<i>Включено</i>' if reactions['admin_bypass'] else '<i>Выключено</i>'}\n\n"
        f"<b>Последних сообщений для реакции:</b> {reactions['last_messages_count']}\n"
        f"<b>Пропускать сообщения:</b> {reactions['ingore_messages'][0]} - {reactions['ingore_messages'][1]}\n\n"
        f"<b>Задержка между реакциями:</b> {reactions['send_delay']} сек\n\n"
        f"<b>Интервал работы:</b>\n"
        f"🕐 <i>{reactions['work_intervals']['active_minutes']}</i> минут работы\n"
        f"⏸️ <i>{reactions['work_intervals']['pause_minutes']}</i> минут паузы\n\n"
        f"<b>Telethon-бот:</b> {'<i>Запущен</i>' if userbot_active else '<i>Остановлен</i>'}\n\n"
        "<b>Вы можете обновить эти настройки в любой момент через меню!</b>\n"
    )

    await message.answer(
        formatted_settings,
        reply_markup=keyboards.settings_menu,
        parse_mode="HTML"
    )
