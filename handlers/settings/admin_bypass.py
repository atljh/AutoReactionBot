from aiogram import types
from aiogram.types import CallbackQuery

from utils import keyboards
from utils.groups import list_groups
from utils.settings import load_settings, save_settings

async def toggle_admin_bypass_handler(callback_query: CallbackQuery):
    await toggle_admin_bypass(callback_query)

async def toggle_admin_bypass(callback_query: types.CallbackQuery):
    settings = load_settings()

    new_status = not settings["reactions"]["admin_bypass"]
    settings["reactions"]["admin_bypass"] = new_status

    save_settings(settings)

    status_text = '<i>Включено</i>' if new_status else '<i>Выключено</i>'

    formatted_settings = (
        "<b>Ваши настройки:</b>\n\n"
        f"<b>Группы:</b> {len(list_groups())} групп\n\n"
        f"<b>Эмодзи для реакций:</b> {', '.join(settings['reactions']['emojis'])}\n"
        f"<b>Рандомные эмодзи:</b> {'<i>Включено</i>' if settings['reactions']['random_emojis'] else '<i>Выключено</i>'}\n\n"
        f"<b>Обход администраторов:</b> {status_text}\n\n"
        f"<b>Пропускать сообщения:</b> {settings['reactions']['ingore_messages'][0]} - {settings['reactions']['ingore_messages'][1]}\n\n"
        f"<b>Интервал работы:</b>\n"
        f"🕐 <i>{settings['reactions']['work_intervals']['active_minutes']}</i> минут работы\n"
        f"⏸️ <i>{settings['reactions']['work_intervals']['pause_minutes']}</i> минут паузы\n\n"
        "<b>Вы можете обновить эти настройки в любой момент через меню!</b>\n"
    )

    await callback_query.message.edit_text(formatted_settings, reply_markup=keyboards.settings_menu, parse_mode="HTML")