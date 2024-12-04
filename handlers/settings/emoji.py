import re
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils.settings import load_settings, save_settings
from utils import keyboards
from states import SetEmojiState
from .settings import settings_handler

emoji_pattern = re.compile("[\U00010000-\U0010FFFF]", flags=re.UNICODE)

async def set_emoji(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработка кнопки для настройки эмодзи для реакции.
    """
    settings = load_settings()

    emojis_list = ", ".join(settings["reactions"]["emojis"]) if settings["reactions"]["emojis"] else "Нет добавленных эмодзи"

    await callback_query.message.edit_text(
        f"<b>Ваши текущие эмодзи для реакции:</b>\n{emojis_list}\n\n"
        "<i>Введите эмодзи, который вы хотите добавить через пробел:</i>\n"
        "<b>Примеры:</b> 😂, ❤️, 👍\n\n"
        "Чтобы отменить, нажмите кнопку ниже.",
        parse_mode="HTML",
        reply_markup=keyboards.choose_emojis,
    )
    await state.set_state(SetEmojiState.waiting_for_emoji)

async def set_emoji_message(message: types.Message, state: FSMContext):
    settings = load_settings()

    emojis_list = ", ".join(settings["reactions"]["emojis"]) if settings["reactions"]["emojis"] else "Нет добавленных эмодзи"

    await message.answer(
        f"<b>Ваши текущие эмодзи для реакции:</b>\n{emojis_list}\n\n"
        "<i>Введите эмодзи, который вы хотите добавить через пробел:</i>\n"
        "<b>Примеры:</b> 😂, ❤️, 👍\n\n"
        "Чтобы отменить, нажмите кнопку ниже.",
        parse_mode="HTML",
        reply_markup=keyboards.choose_emojis,
    )
    await state.set_state(SetEmojiState.waiting_for_emoji)

async def clear_emojis(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработка кнопки для очистки всех эмодзи из списка.
    """
    settings = load_settings()
    emojis = settings["reactions"]["emojis"]
    if not emojis:
        await callback_query.answer()
        return
    else:
        settings["reactions"]["emojis"] = []
    save_settings(settings)

    await state.clear()
    await set_emoji(callback_query, state)

async def process_emoji_input(message: types.Message, state: FSMContext):
    """
    Обработка введенного пользователем эмодзи для добавления в настройки.
    Проверка, что введенный текст является валидным эмодзи.
    """
    input_text = message.text.strip()

    if not input_text:
        await message.answer("Пожалуйста, введите хотя бы одно эмодзи.")
        return

    emojis = input_text.split()

    valid_emojis = [emoji for emoji in emojis if emoji_pattern.match(emoji)]

    if not valid_emojis:
        await message.answer("Пожалуйста, введите хотя бы одно корректное эмодзи.")
        return

    settings = load_settings()

    new_emojis = [emoji for emoji in valid_emojis if emoji not in settings["reactions"]["emojis"]]

    if new_emojis:
        settings["reactions"]["emojis"].extend(new_emojis)
        save_settings(settings)
        await message.answer(f"Эмодзи {', '.join(new_emojis)} успешно добавлены.")
    else:
        await message.answer("Все введенные эмодзи уже есть в списке.")

    await state.clear()
    await set_emoji_message(message, state)


async def toggle_random_emojis_handler(callback_query: types.CallbackQuery):
    settings = load_settings()

    new_status = not settings["reactions"]["random_emojis"]
    settings["reactions"]["random_emojis"] = new_status
    save_settings(settings)

    await settings_handler(callback_query)
