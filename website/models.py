from __future__ import unicode_literals
from collections import defaultdict, Counter

from django.db import models

# Create your models here.



# helper functions

def score_word(a, b):
    """ Scores a word relative to another word. Score is defined as
        the number of letters that match both in value and position."""
    return sum([a[i] == b[i] for i in range(len(a))])

def filter_scores_multiple(scores, guesses):
    """ Filters a scores list multiple times efficiently. Guesses is
        expected to be a list of dictionaries, each having a word and
        feedback key:
            guesses = [
                {"word": str, "feedback": int},
                ...
            ]
    """
    new_words = []
    words = list(s[1] for s in scores)
    for guess in guesses:
        words = filter_words(words, guess['word'], guess['feedback'])
    return score_words(words)

def filter_words(words, guess, correct):
    """ Iterates through words, returning only the words that match
        the given guess the given number of correct letters."""
    new_words = []
    for word in words:
        if correct == -1:
            if guess != word:
                new_words.append(word)
        elif  score_word(word, guess) == correct:
            new_words.append(word)
    return new_words

def filter_scores(scores, guess, correct):
    """ Given a word and it's corresponding score, filters the list
        of scores returning only the scored words that match the given
        score. Returned list will be sorted."""
    words = filter_words([s[1] for s in scores], guess, correct)
    return score_words(words)

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

def request_words(words, feedback):
    response = {'valid': True, 'words': []}
    invalid, msg = validate_words(words)

    if len(invalid) > 0:
        response['valid'] = False
        response['message'] = msg
        for word in words:
            response['words'].append({
                'word': word,
                'valid':  word not in invalid,
                'position': words.index(word)+1
            })
    else:
        response['valid'] = True
        scores = score_words(words)
        for fb in feedback:
            scores = filter_scores(scores, fb['word'], fb['feedback'])
        score_dict = {w[1]: w[0] for w in scores}
        for score, word in scores:
            word_response = {
                'word': word,
                'valid': True,
                'position': words.index(word)+1,
                'score': score_dict[word]
            }
            if word in feedback:
                word_response['feedback'] = feedback[word]
            response['words'].append(word_response)
        for word in words:
            if word not in score_dict:
                word_response = {
                    'word': word,
                    'valid': False,
                    'position': words.index(word)+1
                }
                if word in feedback:
                    word_response['feedback'] = feedback[word]
                response['words'].append(word_response)
    return response
