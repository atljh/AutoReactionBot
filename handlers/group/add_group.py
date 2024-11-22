from aiogram import types
from aiogram.fsm.context import FSMContext
from states import AddGroupStates

from utils import keyboards
from utils.groups import validate_group_link, add_group

async def save_group_name(message: types.Message,  state: FSMContext):
    group_names = message.text.strip().splitlines()
    valid_groups = []

    for group in group_names:
        group = group.strip()
        if group.startswith('https://'):
            group = group[8:]
        if validate_group_link(group):
            add_group(group)
            valid_groups.append(group)
        else:
            await message.answer(f"Некорректная ссылка: <b>{group}</b>. Пропускаем.", parse_mode="HTML")

    if valid_groups:
        await message.answer(
            f"Группа <b>{', '.join(valid_groups)}</b> успешно добавлена!",
            reply_markup=keyboards.main_menu,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "Не было добавлено ни одной группы. Убедитесь, что ссылки имеют правильный формат.",
            reply_markup=keyboards.main_menu,
            parse_mode="HTML"
        )
    await state.clear()

async def add_group_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Введите ссылки на группы в формате\n<b>t.me/group1</b>\n<b>t.me/group2</b>\nКаждую ссылку на новой строке или через пробел.",
        reply_markup=keyboards.back_button,
        parse_mode="HTML"
    )
    await state.set_state(AddGroupStates.waiting_for_group)
