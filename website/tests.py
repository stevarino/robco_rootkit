from django.test import TestCase
from .models import score_word, score_words, filter_scores, validate_words

# Create your tests here.
class FunctionTestCase(TestCase):
    def setUp(self):
        pass

    def test_score_word(self):
        """ score_word should return the number of letters one word shares
            with another."""
        self.assertEqual(1, score_word('a', 'a'))
        self.assertEqual(1, score_word('aa', 'ab'))
        self.assertEqual(1, score_word('ba', 'bb'))
        self.assertEqual(0, score_word('a', 'b'))
        self.assertEqual(0, score_word('ab', 'ba'))
        self.assertEqual(2, score_word('aba', 'cba'))
        self.assertEqual(2, score_word('abc', 'abd'))

    def test_scoring(self):
        """ score_words returns a list of tuples containing score and
            word. Score is determined by comparing each word to every
            other word (including itself) and summing common letters."""
        scores = score_words(['foo', 'far', 'has', 'car'])
        expected = [(7, 'far'), (6, 'car'), (5, 'has'),  (4 , 'foo')]
        self.assertEqual(scores, expected)

    def test_validate_dupes(self):
        """ Ensure duplicates are caught."""
        dupes, msg = validate_words(["foo", "bar", "baz", "foo"])
        self.assertEqual(["foo"], dupes)

    def test_validate_lens(self):
        """ Ensure words of unequal length are caught. Correct length is
            whichever length is the most common."""
        lens, msg = validate_words(["foo", "john", "bar", "baz"])
        self.assertEqual(["john"], lens)

    def test_filter(self):
        """ Check that words which are not possible are filtered."""
        words = ['card', 'fate', 'date', 'daft']
        filtered = filter_scores(score_words(words), 'card', 1)
        self.assertEqual([(9, 'date'), (8, 'fate'), (7, 'daft')], filtered)

    def test_filter_remove(self):
        """ If a word is removed from the  puzzle, don't include it in
            scoring."""
        words = ['cart', 'fate', 'date', 'daft']
        filtered = filter_scores(score_words(words), 'fate', -1)
        self.assertEqual([(8, 'daft'), (7, 'date'), (7, 'cart')], filtered)

    
