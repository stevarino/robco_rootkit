from django.http import HttpResponse, JsonResponse, Http404
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import models

import json
import re

# Create your views here.
import datetime

word_pattern = re.compile('[A-Z]+')

def index(request):
    return render(request, 'website/input.html')

@csrf_exempt
def api(request):
    if not request.is_ajax() or request.method != 'POST':
        raise SuspiciousOperation("No data received.")

    try:
        body = json.loads(request.body)
    except:
        raise SuspiciousOperation("Invalid json request.")

    try:
        assert isinstance(body.get('words'), unicode)

        feedback = body.get('feedback', [])
        assert isinstance(feedback, list)
        for fb in feedback:
            assert isinstance(fb, dict)
            assert isinstance(fb.get('word'), unicode)
            assert isinstance(fb.get('feedback'), int)
    except AssertionError:
        raise SuspiciousOperation("Invalid API request.")


    words = re.findall(word_pattern, body["words"].upper())
    response = models.request_words(words, feedback)
    return JsonResponse(response)
