from tkinter.messagebox import QUESTION

from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import title

# Create your views here.

QUESTION_LIST = [
    {
        'id': i,
        'title': f'Title {i}',
        'text': f'text {i}' * 3,
    } for i in range(30)
]

ANSWER_LIST = [
    {
        'id': i,
        'question_id': i % 30,
        'text': f'ответ  {i} на вопрос {i % 30}',
        'created_at': '2023-10-01',
    } for i in range(50)
]


def index(request):
    page_number = request.GET.get('page', 1)
    page = Paginator(QUESTION_LIST, 3)
    page_obj = page.get_page(page_number)
    return render(request, 'index.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})


def hot(request):
    page_number = request.GET.get('page', 1)
    page = Paginator(QUESTION_LIST[::-1], 3)
    page_obj = page.get_page(page_number)
    return render(request, 'hot.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})


def profile(request):
    return render(request, 'profile.html')


def ask(request):
    return render(request, 'ask.html')


def answer(request, question_id):
    question = next((q for q in QUESTION_LIST if q['id'] == question_id), None)

    answers = [a for a in ANSWER_LIST if a['question_id'] == question_id]

    return render(request, 'answer.html', {
        'question': question,
        'answers': answers
    })


def questions_by_tag(request, tag_name):
    return render(request, 'tag_page.html', {
        'questions': '',
        'tag': tag_name
    })

def register(request):
    return render(request, 'reg.html')

def login(request):
    return render(request, 'login.html')