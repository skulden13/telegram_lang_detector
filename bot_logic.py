import unicodedata

ALLOWED_LETTER_SCRIPTS = (
    "LATIN",
    "GEORGIAN",
)


def contains_letter(text: str) -> bool:
    return any(unicodedata.category(character).startswith("L") for character in text)


def is_allowed_letter(character: str) -> bool:
    character_name = unicodedata.name(character, "")
    return character_name.startswith(ALLOWED_LETTER_SCRIPTS)


def contains_unsupported_letter(text: str) -> bool:
    return any(
        unicodedata.category(character).startswith("L") and not is_allowed_letter(character)
        for character in text
    )


def should_check_language(text: str | None) -> bool:
    return bool(
        text
        and len(text.strip()) >= 3
        and contains_letter(text)
        and contains_unsupported_letter(text)
    )
