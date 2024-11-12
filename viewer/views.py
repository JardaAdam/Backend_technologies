from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
"""Tato finkce vraci pouze return """


def hello(request):
    # http://127.0.0.1:8000/hello/
    return HttpResponse('Hello, World!')


def hello2(request, word):
    # zapis v prohlizeci: http://127.0.0.1:8000/hello2/blue%20nice/
    return HttpResponse(f'Hello, {word} world!')


def hello3(request):
    # zapis v prohlizei: http://127.0.0.1:8000/hello3?word=nice
    word = request.GET.get('word', '')
    return HttpResponse(f'Hello, {word} world!')


def hello4(request):
    # http://127.0.0.1:8000/hello4?word=World
    word = request.GET.get('word', '')
    context = {'word': word}
    return render(request=request, template_name="hello.html", context=context)


def add(request, num1, num2):
    # http://127.0.0.1:8000/add/2/3/
    return HttpResponse(f'{num1} + {num2} = {num1 + num2}')


def add2(request):
    # http://127.0.0.1:8000/add2 -> 0 + 0 = 0
    # http://127.0.0.1:8000/add2?num1=2 -> 2 + 0 = 2
    # http://127.0.0.1:8000/add2?num1=2&num2=3 -> 2 + 3 = 5
    # http://127.0.0.1:8000/add2?num2=2&num1=3 -> 3 + 2 = 5
    num1 = int(request.GET.get('num1', 0))
    num2 = int(request.GET.get('num2', 0))
    return HttpResponse(f'{num1} + {num2} = {num1 + num2}')


def add3(request):
    # http://127.0.0.1:8000/add3?num1=4&num2=6
    num1 = int(request.GET.get('num1', 0))
    num2 = int(request.GET.get('num2', 0))
    result = num1 + num2
    context = {'result': result}
    return render(request=request, template_name="add.html", context=context)
