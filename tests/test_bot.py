import unittest

from bot import check_language


class CheckLanguageTests(unittest.TestCase):
    def test_not_notify_for_text_without_letters(self):
        self.assertFalse(check_language("😬😬😬"))
        self.assertFalse(check_language("12345"))
        self.assertFalse(check_language("123!!!"))
        self.assertFalse(check_language("$$$"))

    def test_not_notify_for_supported_laguages(self):
        self.assertTrue(check_language("გამარჯობა"))
        self.assertTrue(check_language("Hello!"))
        self.assertTrue(check_language("Hola, niños!"))

    def test_notify_for_unsupported_laguages(self):
        self.assertTrue(check_language("Привет!"))
        self.assertTrue(check_language("Мяу"))


if __name__ == "__main__":
    unittest.main()
