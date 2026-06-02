import os
from dotenv import load_dotenv
from bot_logic import should_check_language

load_dotenv()

REPLY_MESSAGE = 'Please use English or Georgian 🇬🇪. Thank you! 🐱❤️'

ALLOWED_LANGUAGE_NAMES = {
    "ENGLISH",
    "GEORGIAN",
}
_detector = None


def check_language(text: str | None) -> bool:
    return should_check_language(text)


def get_detector():
    global _detector

    if _detector is None:
        from lingua import Language, LanguageDetectorBuilder

        _detector = LanguageDetectorBuilder.from_languages(
            Language.ENGLISH,
            Language.GEORGIAN,
            Language.RUSSIAN,
            Language.UKRAINIAN,
            Language.TURKISH,
            Language.ARMENIAN,
        ).build()

    return _detector


async def handle_message(update, context):
    text = update.message.text

    if not check_language(text):
        return

    language = get_detector().detect_language_of(text)

    if language.name not in ALLOWED_LANGUAGE_NAMES:
        await update.message.reply_text(REPLY_MESSAGE)


def main():
    from telegram.ext import Application, MessageHandler, filters

    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    app = Application.builder().token(token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
