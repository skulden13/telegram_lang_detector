import unicodedata


def contains_letter(text: str) -> bool:
    return any(unicodedata.category(character).startswith("L") for character in text)


def should_check_language(text: str | None) -> bool:
    return bool(text and len(text.strip()) >= 3 and contains_letter(text))
