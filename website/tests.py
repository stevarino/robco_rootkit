from django.test import TestCase
from .models import score_word, score_words, filter_scores, validate_words

# Create your tests here.
class FunctionTestCase(TestCase):
    def setUp(self):
        pass

    def test_score_word(self):
        self.assertEqual(1, score_word('a', 'a'))
        self.assertEqual(1, score_word('aa', 'ab'))
        self.assertEqual(1, score_word('ba', 'bb'))
        self.assertEqual(0, score_word('a', 'b'))
        self.assertEqual(0, score_word('ab', 'ba'))
        self.assertEqual(2, score_word('aba', 'cba'))
        self.assertEqual(2, score_word('abc', 'abd'))

    def test_scoring(self):
        pass
