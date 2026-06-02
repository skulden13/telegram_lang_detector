import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from bot import REPLY_MESSAGE, handle_message


class FakeDetector:
    def __init__(self, language_name):
        self.language_name = language_name

    def detect_language_of(self, text):
        return SimpleNamespace(name=self.language_name)


class HandleMessageTests(unittest.IsolatedAsyncioTestCase):
    async def assert_does_not_reply(self, text, language_name="ENGLISH"):
        message = SimpleNamespace(text=text, reply_text=AsyncMock())
        update = SimpleNamespace(message=message)

        with patch("bot.get_detector", return_value=FakeDetector(language_name)):
            await handle_message(update, None)

        message.reply_text.assert_not_called()

    async def assert_replies(self, text, language_name="RUSSIAN"):
        message = SimpleNamespace(text=text, reply_text=AsyncMock())
        update = SimpleNamespace(message=message)

        with patch("bot.get_detector", return_value=FakeDetector(language_name)):
            await handle_message(update, None)

        message.reply_text.assert_awaited_once_with(REPLY_MESSAGE)

    async def test_does_not_notify_for_text_without_letters(self):
        await self.assert_does_not_reply("😬😬😬")
        await self.assert_does_not_reply("12345")
        await self.assert_does_not_reply("123!!!")
        await self.assert_does_not_reply("$$$")

    async def test_does_not_notify_for_supported_languages(self):
        await self.assert_does_not_reply("გამარჯობა", "GEORGIAN")
        await self.assert_does_not_reply("Hello!", "ENGLISH")
        await self.assert_does_not_reply("Hola, niños!", "ENGLISH")
        await self.assert_does_not_reply("💰: 5 lari", "ENGLISH")
        await self.assert_does_not_reply('💰: 5 lari"', "ENGLISH")
        await self.assert_does_not_reply("Price: 5 lari", "ENGLISH")

    async def test_notifies_for_unsupported_languages(self):
        await self.assert_replies("Привет!", "RUSSIAN")
        await self.assert_replies("Мяу", "RUSSIAN")
        await self.assert_replies("💰: 5 лари", "RUSSIAN")
        await self.assert_replies("Price: 5 лари", "RUSSIAN")

    async def test_does_not_detect_language_when_text_should_be_ignored(self):
        message = SimpleNamespace(text='💰: 5 lari"', reply_text=AsyncMock())
        update = SimpleNamespace(message=message)

        detector = Mock()
        with patch("bot.get_detector", return_value=detector):
            await handle_message(update, None)

        detector.detect_language_of.assert_not_called()
        message.reply_text.assert_not_called()


if __name__ == "__main__":
    unittest.main()
