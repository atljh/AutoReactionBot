from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="➕ Добавить аккаунт", callback_data="add_account")],
    [InlineKeyboardButton(text="📜 Показать аккаунты", callback_data="view_accounts")],
    [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
    [InlineKeyboardButton(text="🚀 Запустить софт", callback_data="start_software")],
    [InlineKeyboardButton(text="🛑 Остановить софт", callback_data="stop_software")],
])


settings_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📋 Настройки групп", callback_data="view_groups"),
    ],
    [
        InlineKeyboardButton(text="🎭 Настройки реакций", callback_data="set_emoji"),
        InlineKeyboardButton(text="🕒 Время работы", callback_data="set_work_interval"),
    ],
    [
        InlineKeyboardButton(text="⏭️ Пропуск сообщений", callback_data="set_ignore_messages"),
        InlineKeyboardButton(text="💯 Последних сообщений", callback_data="set_last_messages"),
    ],    
    [
        InlineKeyboardButton(text="⚙️ Обход админов: Вкл/Выкл", callback_data="toggle_admin_bypass"),
        InlineKeyboardButton(text="🎲 Рандомные эмодзи: Вкл/Выкл", callback_data="toggle_random_emojis"),
    ],
    [
        InlineKeyboardButton(text="💤 Задержка реакций", callback_data="send_delay"),
        InlineKeyboardButton(text="🔄 Перезагрузить софт", callback_data="restart_bot"),
    ],
    [
        InlineKeyboardButton(text="Администраторы", callback_data="list_admin"),
        InlineKeyboardButton(text="Прокси", callback_data="view_proxy")

    ],
    [
        InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")
    ],
])

choose_emojis = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Удалить все эмодзи", callback_data="emoji_clear"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="settings")
        ],
        
    ]
)

proxy_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"➕ Добавить прокси",
                callback_data=f"add_proxy",
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="settings"
            )
        ]
    ]
)

admin_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"➕ Добавить админа",
                callback_data=f"add_admin",
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="settings"
            )
        ]
    ]
)



back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ]
)

back_settings_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="settings")]
    ]
)


cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
    ]
)

cancel_settings_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="settings")]
    ]
)
add_group_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Добавить группу", callback_data="add_group"),
            InlineKeyboardButton(text="Выбрать активную группу", callback_data="select_group"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")
        ]
    ]
)
