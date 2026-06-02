import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from lingua import Language, LanguageDetectorBuilder
from dotenv import load_dotenv
from bot_logic import should_check_language

load_dotenv()

ALLOWED_LANGUAGES = {
    Language.ENGLISH,
    Language.GEORGIAN,
}

detector = LanguageDetectorBuilder.from_languages(
    Language.ENGLISH,
    Language.GEORGIAN,
    Language.RUSSIAN,
    Language.UKRAINIAN,
    Language.TURKISH,
    Language.ARMENIAN,
).build()

REPLY_MESSAGE = 'Please use English or Georgian 🇬🇪. Thank you! 🐱❤️'


async def check_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not should_check_language(text):
        return

    language = detector.detect_language_of(text)

    if language not in ALLOWED_LANGUAGES:
        await update.message.reply_text(REPLY_MESSAGE)


def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    app = Application.builder().token(token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_language))

    app.run_polling()


if __name__ == "__main__":
    main()
