from aiogram import Dispatcher, types
import utils.keyboards as keyboards
from services.emoji_service import process_emoji_selection

async def setup_reactions(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Выберите эмодзи для реакций:",
        reply_markup=keyboards.choose_emojis
    )

def register_emoji_handlers(dp: Dispatcher):
    dp.callback_query.register(setup_reactions, lambda c: c.data == "setup_reactions")
    dp.callback_query.register(process_emoji_selection, lambda c: c.data.startswith("emoji_"))
