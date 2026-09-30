import unicodedata

ALLOWED_LETTER_SCRIPTS = ("GEORGIAN",)
ALLOWED_LETTER_NAMES = ("INFORMATION SOURCE",)


def contains_letter(text: str) -> bool:
    normalized_text = unicodedata.normalize("NFC", text)
    return any(unicodedata.category(character).startswith("L") for character in normalized_text)


def is_allowed_letter(character: str) -> bool:
    if "A" <= character <= "Z" or "a" <= character <= "z":
        return True

    character_name = unicodedata.name(character, "")
    return (
        character_name in ALLOWED_LETTER_NAMES
        or character_name.startswith(ALLOWED_LETTER_SCRIPTS)
    )


def contains_unsupported_letter(text: str) -> bool:
    normalized_text = unicodedata.normalize("NFC", text)
    return any(
        unicodedata.category(character).startswith("L") and not is_allowed_letter(character)
        for character in normalized_text
    )


def should_check_language(text: str | None) -> bool:
    return bool(
        text
        and len(text.strip()) >= 3
        and contains_letter(text)
        and contains_unsupported_letter(text)
    )
