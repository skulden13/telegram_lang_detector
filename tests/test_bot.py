import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot import REPLY_MESSAGE, handle_message


class HandleMessageTests(unittest.IsolatedAsyncioTestCase):
    async def assert_does_not_reply(self, text):
        message = SimpleNamespace(text=text, reply_text=AsyncMock())
        update = SimpleNamespace(message=message)

        await handle_message(update, None)

        message.reply_text.assert_not_called()

    async def assert_replies(self, text):
        message = SimpleNamespace(text=text, reply_text=AsyncMock())
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
        await self.assert_does_not_reply("Hola, niños!")
        await self.assert_does_not_reply("💰: 5 lari")
        await self.assert_does_not_reply('💰: 5 lari"')
        await self.assert_does_not_reply("Price: 5 lari")

    async def test_notifies_for_unsupported_scripts(self):
        await self.assert_replies("Привет!")
        await self.assert_replies("Мяу")
        await self.assert_replies("💰: 5 лари")
        await self.assert_replies("Price: 5 лари")
        await self.assert_replies("Price: 10 лари")


if __name__ == "__main__":
    unittest.main()
