from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить аккаунт", callback_data="add_account")],
        [InlineKeyboardButton(text="📜 Показать аккаунты", callback_data="view_accounts")],
        [InlineKeyboardButton(text="Настроить группы", callback_data="view_groups")],
        [InlineKeyboardButton(text="⚙️ Настроить реакции", callback_data="setup_reactions")],
        [InlineKeyboardButton(text="🔄 Перезагрузить софт", callback_data="restart_bot")]
    ]
)

choose_emojis = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="😂", callback_data="emoji_😂"),
            InlineKeyboardButton(text="❤️", callback_data="emoji_❤️")
        ],
        [
            InlineKeyboardButton(text="👍", callback_data="emoji_👍"),
            InlineKeyboardButton(text="🔥", callback_data="emoji_🔥")
        ],
        [
            InlineKeyboardButton(text="✅ Завершить выбор", callback_data="emoji_done")
        ]
    ]
)

back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ]
)

cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
    ]
)

add_group_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить группу", callback_data="add_group"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")
        ]
    ]
)
