from django.http import HttpResponse, JsonResponse, Http404
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import re

from . import models

# Create your views here.
import datetime

word_pattern = re.compile('[A-Z]+')

def index(request):
    return render(request, 'website/input.html')

@csrf_exempt
def api(request):
    if request.is_ajax() and request.method == 'POST':
        body = json.loads(request.body)
    if "words" not in body:
        raise SuspiciousOperation("Did not receive word list.")
    response = {'valid': True, 'words': []}
    words = re.findall(word_pattern, body["words"].upper())
    invalid, msg = models.validate_words(words)

    if len(invalid) > 0:
        response['valid'] = False
        response['message'] = msg
        for word in words:
            word_response = {'word': word}
            if word in invalid:
                 word_response['invalid'] = True
            response['words'].append(word_response)
    else:
        scores = models.score_words(words)
        for score, word in scores:
            word_response = {
                'word': word,
                'score': score,
                'position': "{}/{}".format(words.index(word)+1, len(words))
            }

            response['words'].append(word_response)
    return JsonResponse(response)
