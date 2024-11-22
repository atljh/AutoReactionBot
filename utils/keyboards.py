from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить аккаунт", callback_data="add_account")],
        [InlineKeyboardButton(text="📜 Показать аккаунты", callback_data="show_accounts")],
        [InlineKeyboardButton(text="❌ Удалить аккаунт", callback_data="delete_account")],
        [InlineKeyboardButton(text="⚙️ Настроить реакции", callback_data="setup_reactions")],
        [InlineKeyboardButton(text="🔄 Перезагрузить софт", callback_data="restart_bot")]
    ]
)

choose_emojis = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="😂", callback_data="emoji_😂"), InlineKeyboardButton(text="❤️", callback_data="emoji_❤️")],
        [InlineKeyboardButton(text="👍", callback_data="emoji_👍"), InlineKeyboardButton(text="🔥", callback_data="emoji_🔥")],
        [InlineKeyboardButton(text="✅ Завершить выбор", callback_data="emoji_done")]
    ]
)

back_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]]
)

cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
    ]
)