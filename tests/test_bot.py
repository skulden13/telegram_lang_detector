import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot import REPLY_MESSAGE, handle_message


class HandleMessageTests(unittest.IsolatedAsyncioTestCase):
    async def assert_does_not_reply(self, text=None, quoted_text=None, caption=None):
        quote = SimpleNamespace(text=quoted_text) if quoted_text is not None else None
        message = SimpleNamespace(text=text, caption=caption, quote=quote, reply_text=AsyncMock())
        update = SimpleNamespace(message=message)

        await handle_message(update, None)

        message.reply_text.assert_not_called()

    async def assert_replies(self, text=None, quoted_text=None, caption=None):
        quote = SimpleNamespace(text=quoted_text) if quoted_text is not None else None
        message = SimpleNamespace(text=text, caption=caption, quote=quote, reply_text=AsyncMock())
        update = SimpleNamespace(message=message)

        await handle_message(update, None)

        message.reply_text.assert_awaited_once_with(REPLY_MESSAGE)

    async def test_does_not_notify_for_text_without_letters(self):
        await self.assert_does_not_reply("😬😬😬")
        await self.assert_does_not_reply("12345")
        await self.assert_does_not_reply("123!!!")
        await self.assert_does_not_reply("$$$")

    async def test_does_not_notify_for_supported_scripts(self):
        await self.assert_does_not_reply("გამარჯობა")
        await self.assert_does_not_reply("Hello!")
        await self.assert_does_not_reply("💰: 5 lari")
        await self.assert_does_not_reply('💰: 5 lari"')
        await self.assert_does_not_reply("Price: 5 lari")

    async def test_notifies_for_unsupported_scripts(self):
        await self.assert_replies("Привет!")
        await self.assert_replies("Мяу")
        await self.assert_replies("💰: 5 лари")
        await self.assert_replies("Price: 5 лари")
        await self.assert_replies("Price: 10 лари")

    async def test_notifies_for_photo_caption_with_unsupported_script(self):
        await self.assert_replies(
            caption="ECCO Receptor походные водонепроницаемые ботинки с GoreTex"
        )

    async def test_does_not_notify_for_photo_caption_with_supported_scripts(self):
        await self.assert_does_not_reply(caption="ECCO shoes, size: 41, price: 40 lari")

    async def test_notifies_when_quoted_text_contains_unsupported_script(self):
        await self.assert_replies("test", quoted_text="бегала один раз маленькую пробежку")

    async def test_does_not_notify_when_quote_uses_supported_scripts(self):
        await self.assert_does_not_reply("test", quoted_text="Hello გამარჯობა")

    async def test_notifies_for_turkish_text_with_unsupported_latin_letters(self):
        await self.assert_replies("Hayırlı akşamlar")
        await self.assert_replies("çok güzel")

    async def test_notifies_for_german_text_with_unsupported_latin_letters(self):
        await self.assert_replies("schöne Grüße")

    async def test_notifies_for_extended_latin_text(self):
        await self.assert_replies("Cześć")
        await self.assert_replies("Dobrý večer")
        await self.assert_replies("Ça va très bien")
        await self.assert_replies("Hola, niños!")
        await self.assert_replies("Olá, tudo bem?")
        await self.assert_replies("Bună seara")
        await self.assert_replies("God kväll")
        await self.assert_replies("Góðan daginn")
        await self.assert_replies("Xin chào")


if __name__ == "__main__":
    unittest.main()
