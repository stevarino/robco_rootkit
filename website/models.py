from __future__ import unicode_literals
from collections import defaultdict, Counter

from django.db import models

# Create your models here.



# helper functions

def score_word(a, b):
    """ Scores a word relative to another word. Score is defined as
        the number of letters that match both in value and position."""
    return sum([a[i] == b[i] for i in range(len(a))])

def filter_scores(scores, guess, correct):
    """ Given a word and it's corresponding score, filters the list
        of scores returning only the scored words that match the given score."""
    new_words = []
    for score, word in scores:
        score = score_word(word, guess)
        if score == correct:
            new_words.append(word)

    return score_words(new_words)


def score_words(words):
    """ Returns a list of tuples (int score, str word) ordered by score
        desc. Score is defined by how similar two words are."""
    scores = []
    for word in words:
        score = 0
        for other_word in words:
            score += score_word(word, other_word)

        scores.append((score, word))

    return sorted(scores, key=lambda tup: tup[0], reverse=True)

def validate_words(words):
    """ Returns a tuple consisting of a list of words that do not match the
        criteria (unequal lengths or duplicates) and a message regarding the
        error. Note: not definitive."""
    lens = defaultdict(list)
    for word in words:
        lens[len(word)].append(word)

    wrong_words = []
    if (len(lens) > 1):
        for suspects in lens.values():
            if len(suspects) < len(wrong_words) or len(wrong_words) == 0:
                wrong_words = suspects
    if len(wrong_words) > 0:
        return wrong_words, "Words have unequal lengths."

    duplicates = [item for item, count in Counter(words).items() if count > 1]

    if len(duplicates) > 0:
        return duplicates, "Duplicate words found."

    return [], ""
