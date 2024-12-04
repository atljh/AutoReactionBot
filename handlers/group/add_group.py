from aiogram import types
from aiogram.fsm.context import FSMContext

from utils import keyboards
from utils.groups import add_group
from .view_group import view_groups_message
from states import AddGroupStates

async def save_group_name(message: types.Message,  state: FSMContext):
    group_names = message.text.strip().splitlines()
    valid_groups = []

    for group in group_names:
        group = group.strip()
        if group.startswith('https://'):
            group = group[8:]
        add_group(group)
        valid_groups.append(group)

    if valid_groups:
        await message.answer(
            f"Группа <b>{', '.join(valid_groups)}</b> успешно добавлена!",
            parse_mode="HTML"
        )
        await view_groups_message(message)
    else:
        await message.answer(
            "Не было добавлено ни одной группы. Убедитесь, что ссылки имеют правильный формат.",
            parse_mode="HTML"
        )
        await view_groups_message(message)
    await state.clear()
    
async def add_group_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Введите ссылки на группы или id закрытого канала в формате\n<b>t.me/group1</b>\n<b>t.me/group2</b>\nКаждую ссылку на новой строке или через пробел.",
        reply_markup=keyboards.back_settings_button,
        parse_mode="HTML"
    )
    await state.set_state(AddGroupStates.waiting_for_group)
