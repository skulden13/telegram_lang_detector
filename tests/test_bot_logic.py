import unittest

from bot_logic import contains_letter, contains_unsupported_letter, is_allowed_letter, should_check_language


class ContainsLetterTests(unittest.TestCase):
    def test_returns_false_for_emoji_only_text(self):
        self.assertFalse(contains_letter("😬😬😬"))

    def test_returns_false_for_numbers_and_punctuation(self):
        self.assertFalse(contains_letter("123!!!"))

    def test_returns_true_for_latin_text_with_emoji(self):
        self.assertTrue(contains_letter("hello 😬"))

    def test_returns_true_for_georgian_text_with_flag(self):
        self.assertTrue(contains_letter("გამარჯობა 🇬🇪"))


class AllowedLetterTests(unittest.TestCase):
    def test_returns_true_for_ascii_latin_letters(self):
        self.assertTrue(is_allowed_letter("a"))
        self.assertTrue(is_allowed_letter("Z"))

    def test_returns_false_for_extended_latin_letters(self):
        extended_latin_letters_by_language = {
            "Turkish": "çğıİöşü",
            "German": "äöüß",
            "Polish": "ąćęłńóśźż",
            "Czech": "čďěňřšťž",
            "French": "àâçéèêëîïôùûüÿœ",
            "Spanish": "áéíñóúü",
            "Portuguese": "áâãàçéêíóôõú",
            "Romanian": "ăâîșț",
            "Nordic": "åäæøö",
            "Icelandic": "áðéíóúýþæö",
            "Vietnamese": "ăâđêôơưáàảãạấầẩẫậắằẳẵặếềểễệớờởỡợứừửữự",
        }

        for language, letters in extended_latin_letters_by_language.items():
            with self.subTest(language=language):
                for letter in letters:
                    self.assertFalse(is_allowed_letter(letter))

    def test_returns_true_for_georgian_letters(self):
        self.assertTrue(is_allowed_letter("ა"))

    def test_returns_false_for_unsupported_letters(self):
        self.assertFalse(is_allowed_letter("п"))
        self.assertFalse(is_allowed_letter("ա"))


class ContainsUnsupportedLetterTests(unittest.TestCase):
    def test_returns_false_for_latin_and_georgian_text(self):
        self.assertFalse(contains_unsupported_letter("Hello!"))
        self.assertFalse(contains_unsupported_letter("გამარჯობა"))
        self.assertFalse(contains_unsupported_letter('💰: 5 lari'))
        self.assertFalse(contains_unsupported_letter('💰: 5 lari"'))

    def test_returns_true_for_unsupported_letter_scripts(self):
        self.assertTrue(contains_unsupported_letter("Привет!"))
        self.assertTrue(contains_unsupported_letter("За 5 лари"))
        self.assertTrue(contains_unsupported_letter("Price: 5 лари"))

    def test_returns_true_for_unsupported_latin_letters(self):
        self.assertTrue(contains_unsupported_letter("Hayırlı akşamlar"))
        self.assertTrue(contains_unsupported_letter("çok güzel"))
        self.assertTrue(contains_unsupported_letter("schöne Grüße"))
        self.assertTrue(contains_unsupported_letter("Cześć"))
        self.assertTrue(contains_unsupported_letter("Dobrý večer"))
        self.assertTrue(contains_unsupported_letter("Ça va très bien"))
        self.assertTrue(contains_unsupported_letter("Hola, niños!"))
        self.assertTrue(contains_unsupported_letter("Olá, tudo bem?"))
        self.assertTrue(contains_unsupported_letter("Bună seara"))
        self.assertTrue(contains_unsupported_letter("God kväll"))
        self.assertTrue(contains_unsupported_letter("Góðan daginn"))
        self.assertTrue(contains_unsupported_letter("Xin chào"))
        self.assertTrue(contains_unsupported_letter("Xin chào"))


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

    def test_returns_false_for_ascii_latin_or_georgian_text(self):
        self.assertFalse(should_check_language("hey"))
        self.assertFalse(should_check_language("hello 123"))
        self.assertFalse(should_check_language("გამარჯობა"))
        self.assertFalse(should_check_language("💰: 5 lari"))
        self.assertFalse(should_check_language('💰: 5 lari"'))

    def test_returns_true_for_unsupported_letter_scripts(self):
        self.assertTrue(should_check_language("Привет!"))
        self.assertTrue(contains_unsupported_letter("За 5 лари"))
        self.assertTrue(should_check_language("Price: 5 лари"))
        self.assertTrue(should_check_language("Price: 10 лари"))

    def test_returns_true_for_turkish_text_with_unsupported_latin_letters(self):
        self.assertTrue(should_check_language("Hayırlı akşamlar"))
        self.assertTrue(should_check_language("çok güzel"))

    def test_returns_true_for_german_text_with_unsupported_latin_letters(self):
        self.assertTrue(should_check_language("schöne Grüße"))

    def test_returns_true_for_extended_latin_text(self):
        self.assertTrue(should_check_language("Cześć"))
        self.assertTrue(should_check_language("Dobrý večer"))
        self.assertTrue(should_check_language("Ça va très bien"))
        self.assertTrue(should_check_language("Hola, niños!"))
        self.assertTrue(should_check_language("Olá, tudo bem?"))
        self.assertTrue(should_check_language("Bună seara"))
        self.assertTrue(should_check_language("God kväll"))
        self.assertTrue(should_check_language("Góðan daginn"))
        self.assertTrue(should_check_language("Xin chào"))
        self.assertTrue(should_check_language("Xin chào"))


if __name__ == "__main__":
    unittest.main()
