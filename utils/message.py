from aiogram.types import Message

def can_edit_message(message: Message) -> bool:
    """
    Checks if a message can be edited.
    
    Args:
        message (Message): The Telegram message object.
    
    Returns:
        bool: True if the message can be edited, False otherwise.
    """
    # Only text messages or messages with a caption are editable
    if not message.text and not message.caption:
        return False

    # Only the bot or the original sender can edit the message
    if not message.from_user or not message.from_user.is_bot:
        return False

    # Telegram's 48-hour editing limit
    time_since_sent = message.date - message.edit_date if message.edit_date else 0
    if time_since_sent.total_seconds() > 48 * 3600:
        return False

    return True