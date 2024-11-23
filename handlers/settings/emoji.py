from aiogram import types
from aiogram.types import CallbackQuery

import utils.keyboards as keyboards
from utils.settings import load_settings, save_settings
from utils.groups import list_groups

async def setup_reactions(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Выберите эмодзи для реакций:",
        reply_markup=keyboards.choose_emojis
    )

chosen_emojis = []

async def process_emoji_selection(callback_query: types.CallbackQuery):
    settings = load_settings()
    chosen_emojis = settings["reactions"].get("emojis", [])

    emoji = callback_query.data.split("_")[1]
    if emoji == "done":
        if not chosen_emojis:
            await callback_query.message.answer("Вы не выбрали ни одного эмодзи.")
        else:
            await callback_query.message.answer(
                f"Выбранные эмодзи сохранены: {', '.join(chosen_emojis)}"
            )
    elif emoji == "clear":
        settings["reactions"]["emojis"] = []
        save_settings(settings)
        await callback_query.message.answer("Все эмодзи удалены.")
    else:
        if emoji not in chosen_emojis:
            chosen_emojis.append(emoji)
            settings["reactions"]["emojis"] = chosen_emojis
            save_settings(settings)
            await callback_query.answer(f"Вы добавили: {emoji}")
        else:
            await callback_query.answer(f"Эмодзи {emoji} уже выбрано.")


async def toggle_random_emojis_handler(callback_query: CallbackQuery):
    await toggle_random_emojis(callback_query)

async def toggle_random_emojis(callback_query: types.CallbackQuery):
    settings = load_settings()

    new_status = not settings["reactions"]["random_emojis"]
    settings["reactions"]["random_emojis"] = new_status

    save_settings(settings)

    status_text = '<i>Включено</i>' if new_status else '<i>Выключено</i>'

    formatted_settings = (
        "<b>Ваши настройки:</b>\n\n"
        f"<b>Группы:</b> {len(list_groups())} групп\n\n"
        f"<b>Эмодзи для реакций:</b> {', '.join(settings['reactions']['emojis'])}\n"
        f"<b>Рандомные эмодзи:</b> {status_text}\n\n"
        f"<b>Обход администраторов:</b> {'<i>Включёно</i>' if settings['reactions']['admin_bypass'] else '<i>Выключено</i>'}\n\n"
        f"<b>Пропускать сообщения:</b> {settings['reactions']['ingore_messages'][0]} - {settings['reactions']['ingore_messages'][1]}\n\n"
        f"<b>Интервал работы:</b>\n"
        f"🕐 <i>{settings['reactions']['work_intervals']['active_minutes']}</i> минут работы\n"
        f"⏸️ <i>{settings['reactions']['work_intervals']['pause_minutes']}</i> минут паузы\n\n"
        "<b>Вы можете обновить эти настройки в любой момент через меню!</b>\n"
    )

    await callback_query.message.edit_text(formatted_settings, reply_markup=keyboards.settings_menu, parse_mode="HTML")
