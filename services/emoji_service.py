from rich.console import Console

console = Console()
chosen_emojis = []

async def process_emoji_selection(callback_query):
    global chosen_emojis

    emoji = callback_query.data.split("_")[1]
    if emoji == "done":
        await callback_query.message.answer(f"Выбранные эмодзи: {', '.join(chosen_emojis)}")
        console.log(f"[green]Итоговый выбор: {chosen_emojis}[/green]")
        chosen_emojis = []
    else:
        if emoji not in chosen_emojis:
            chosen_emojis.append(emoji)
        await callback_query.answer(f"Вы добавили: {emoji}")
        console.log(f"[blue]Добавлено эмодзи: {emoji}[/blue]")
