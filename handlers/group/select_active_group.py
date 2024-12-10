from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.groups import list_groups, get_active_group, set_active_group, delete_active_group

async def select_group_handler(callback_query: types.CallbackQuery):
    """
    Хэндлер для выбора активной группы.
    """
    groups = list_groups()

    if not groups:
        await callback_query.message.edit_text(
            "❌ Нет доступных групп для выбора.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➕ Добавить группу", callback_data="add_group")],
                    [InlineKeyboardButton(text="⬅️ Назад", callback_data="view_groups")]
                ]
            )
        )
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for group in groups:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"{group}",
                callback_data=f"activate_group_{group}"
            )
        ])

    active_group = get_active_group()
    if not active_group:
        message_text = 'Нет активной группы, выберите группу для реакций:'
    else:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="Удалить активную группу", callback_data="delete_active_group")]
        )
        message_text = f'Активная группа {active_group}\nИзменить:'

    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="view_groups")]
    )

    await callback_query.message.edit_text(
        message_text,
        reply_markup=keyboard
    )

async def activate_group_handler(callback_query: types.CallbackQuery):
    group = callback_query.data.split('_')[-1]

    set_active_group(group)

    await callback_query.answer(
        f"Активная группа {group} установлена"
    )
    await select_group_handler(callback_query)

async def delete_active_group_handler(callback_query: types.CallbackQuery):

    delete_active_group()

    await callback_query.answer(
        f"Активная группа удалена"
    )
    await select_group_handler(callback_query)