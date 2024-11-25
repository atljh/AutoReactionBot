import emoji

def is_valid_emoji(emoticon):
    return emoji.is_emoji(emoticon)

def filter_valid_emojis(emojis):
    return [e for e in emojis if is_valid_emoji(e)]

