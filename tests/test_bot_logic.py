import unittest

from bot_logic import contains_letter, should_check_language


class ContainsLetterTests(unittest.TestCase):
    def test_returns_false_for_emoji_only_text(self):
        self.assertFalse(contains_letter("😬😬😬"))

    def test_returns_false_for_numbers_and_punctuation(self):
        self.assertFalse(contains_letter("123!!!"))

    def test_returns_true_for_english_text_with_emoji(self):
        self.assertTrue(contains_letter("hello 😬"))

    def test_returns_true_for_georgian_text_with_flag(self):
        self.assertTrue(contains_letter("გამარჯობა 🇬🇪"))


class ShouldCheckLanguageTests(unittest.TestCase):
    def test_returns_false_for_empty_or_short_text(self):
        self.assertFalse(should_check_language(None))
        self.assertFalse(should_check_language(""))
        self.assertFalse(should_check_language("hi"))

    def test_returns_false_for_text_without_letters(self):
        self.assertFalse(should_check_language("😬😬😬"))
        self.assertFalse(should_check_language("12345"))
        self.assertFalse(should_check_language("123!!!"))
        self.assertFalse(should_check_language("$$$"))

    def test_returns_true_for_supported_length_text_with_letters(self):
        self.assertTrue(should_check_language("hey"))
        self.assertTrue(should_check_language("გამარჯობა"))

    def test_returns_true_for_text_with_letters_and_numbers(self):
        self.assertTrue(should_check_language("hello 123"))


if __name__ == "__main__":
    unittest.main()
