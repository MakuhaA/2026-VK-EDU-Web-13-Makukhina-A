from django.shortcuts import render, get_object_or_404
from .models import Question, Answer, Tag
from .utils import paginate
from django.db.models import Count


def index(request):
    questions = Question.objects.new()

    page_obj = paginate(questions, request, per_page=3)

    return render(request, 'index.html', context={'page_obj': page_obj})


def hot(request):
    questions = Question.objects.best()

    page_obj = paginate(questions, request, per_page=3)

    return render(request, 'hot.html', context={'page_obj': page_obj})


def questions_by_tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    page_obj = paginate(questions, request, per_page=3)
    return render(request, 'tag_page.html', {
        'page_obj': page_obj,
        'tag': tag_name
    })


def answer(request, question_id):
    question = get_object_or_404(Question.objects.select_related('author').annotate(num_likes=Count('question_likes')), id=question_id)

    answers = question.answers.select_related('author__profile').all()

    return render(request, 'answer.html', {
        'question': question,
        'answers': answers
    })


def profile(request):
    return render(request, 'profile.html')


def ask(request):
    return render(request, 'ask.html')


def register(request):
    return render(request, 'reg.html')


def login(request):
    return render(request, 'login.html')
