import os
from dotenv import load_dotenv
from bot_logic import should_check_language

load_dotenv()

REPLY_MESSAGE = 'Please use English or Georgian 🇬🇪. Thank you! 🐱❤️'


def check_language(text: str | None) -> bool:
    return should_check_language(text)


async def handle_message(update, context):
    message = update.message
    text = message.text
    quote = getattr(message, "quote", None)
    quoted_text = getattr(quote, "text", None)

    if not (check_language(text) or check_language(quoted_text)):
        return

    await message.reply_text(REPLY_MESSAGE)


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
