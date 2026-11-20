from PIL.Image import Image
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from core.forms import LoginForms, RegisterForm, ProfileForm
from django.views.decorators.http import require_POST

from .forms import QuestionForm, AnswerForm, ImageForm
from .models import Question, Answer, Tag, QuestionLike, ImageModel, AnswerLike
from core.models import Profile
from .utils import paginate
from django.db.models import Count


def index(request):
    questions = Question.objects.new()
    page_obj = paginate(questions, request, per_page=3)

    liked_questions_ids = []
    if request.user.is_authenticated:
        liked_questions_ids = QuestionLike.objects.filter(
            user=request.user
        ).values_list('question_id', flat=True)

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'liked_questions_ids': liked_questions_ids
    })


def hot(request):
    questions = Question.objects.best()
    page_obj = paginate(questions, request, per_page=3)

    liked_questions_ids = []
    if request.user.is_authenticated:
        liked_questions_ids = QuestionLike.objects.filter(
            user=request.user
        ).values_list('question_id', flat=True)

    return render(request, 'hot.html', {
        'page_obj': page_obj,
        'liked_questions_ids': liked_questions_ids
    })


def questions_by_tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    page_obj = paginate(questions, request, per_page=3)

    liked_questions_ids = []
    if request.user.is_authenticated:
        liked_questions_ids = QuestionLike.objects.filter(
            user=request.user
        ).values_list('question_id', flat=True)

    return render(request, 'tag_page.html', {
        'page_obj': page_obj,
        'tag': tag_name,
        'liked_questions_ids': liked_questions_ids
    })


def answer(request, question_id):
    question = get_object_or_404(Question.objects.select_related('author')
                                 .prefetch_related('tags')
                                 .annotate(num_likes=Count('question_likes')), id=question_id)
    answers = question.answers.all()

    liked_answers_ids = []
    liked_questions_ids = []

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = AnswerForm(request.POST, user=request.user, question=question)
        if form.is_valid():
            answer = form.save()
            return redirect(f"{question.get_absolute_url()}#answer-{answer.pk}")
    else:
        form = AnswerForm()

    if request.user.is_authenticated:
        liked_answers_ids = AnswerLike.objects.filter(
            user=request.user,
            answer__in=answers
        ).values_list('answer_id', flat=True)

        liked_questions_ids = QuestionLike.objects.filter(
            user=request.user,
            question=question
        ).values_list('question_id', flat=True)

    answers = question.answers.select_related('author__profile').all()

    return render(request, 'answer.html', {
        'question': question,
        'answers': answers,
        'form': form,
        'liked_answers_ids': liked_answers_ids,
        'liked_questions_ids': liked_questions_ids
    })

@login_required(login_url='/login')
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            if 'image' in request.FILES:
                image_obj = ImageModel.objects.create(
                    image=request.FILES['image'],
                    user=request.user,
                    title=f"Картинка к вопросу: {question.title[:50]}"
                )
                question.image = image_obj
            question = form.save()

            return redirect('answer', question_id=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'form': form})


@login_required(login_url='/login')
def like_question(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)

        like, created = QuestionLike.objects.get_or_create(
            user=request.user,
            question=question
        )

        if not created:
            like.delete()


    return redirect(request.META.get('HTTP_REFERER', 'index'))


def images(request):
    user = request.user
    image = ImageForm.object.all()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('images'))

    else:
        form = ImageForm(user)

    return redirect(request, 'images.html', context={'form':form, 'image': image })


@login_required(login_url='/login')
def like_answer(request, answer_id):
    if request.method == 'POST':
        answer = get_object_or_404(Answer, id=answer_id)

        like, created = AnswerLike.objects.get_or_create(
            user=request.user,
            answer=answer
        )

        if not created:
            like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'index'))

@require_POST
@login_required(login_url='/login')
def like_question_async(request, question_id):
    question = Question.objects.annotate(likes_count=Count('question_likes')).filter(id=question_id).first()

    if question:
        question_like, created = QuestionLike.objects.get_or_create(question=question, user=request.user)
        if not created:
            question_like.delete()

        new_count = question.question_likes.count()
        return JsonResponse({'count': new_count})

    return JsonResponse({'error': 'Вопрос не найден'}, status=404)


@require_POST
@login_required(login_url='/login')
def like_answer_async(request, answer_id):
    answer = Answer.objects.annotate(likes_count=Count('answer_likes')).filter(id=answer_id).first()

    if answer:
        answer_like, created = AnswerLike.objects.get_or_create(answer=answer, user=request.user)

        if not created:
            answer_like.delete()
            liked = False
        else:
            liked = True

        new_count = answer.answer_likes.count()
        return JsonResponse({'count': new_count, 'liked': liked})

    return JsonResponse({'error': 'Ответ не найден'}, status=404)


@require_POST
@login_required(login_url='/login')
def like_question_async(request, question_id):
    question = Question.objects.annotate(likes_count=Count('question_likes')).filter(id=question_id).first()

    if question:
        question_like, created = QuestionLike.objects.get_or_create(question=question, user=request.user)

        if not created:
            question_like.delete()
            liked = False
        else:
            liked = True

        new_count = question.question_likes.count()
        return JsonResponse({'count': new_count, 'liked': liked})

    return JsonResponse({'error': 'Вопрос не найден'}, status=404)


@require_POST
@login_required(login_url='/login')
def mark_correct_answer(request, question_id, answer_id):
    question = get_object_or_404(Question, id=question_id)

    if question.author != request.user:
        return JsonResponse({'error': 'Только автор вопроса может выбрать правильный ответ'}, status=403)

    answer = get_object_or_404(Answer, id=answer_id, question=question)

    question.answers.update(is_correct=False)
    answer.is_correct = True
    answer.save()

    return JsonResponse({'success': True})