from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.urls import reverse
from core.models import Profile


class QuestionManager(models.Manager):
    def new(self):
        return self.select_related('author').prefetch_related('tags').annotate(
            num_likes=models.Count('question_likes')).order_by('-created_at')

    def best(self):
        return self.select_related('author').prefetch_related('tags').annotate(
            num_likes=models.Count('question_likes')).order_by('-num_likes')

    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).select_related('author').prefetch_related('tags').annotate(
            num_likes=models.Count('question_likes'))

class ImageModel(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    image = models.ForeignKey(ImageModel, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def get_absolute_url(self):
        return reverse('answer', kwargs={'question_id': self.pk})

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', verbose_name="Автор")
    content = models.TextField(verbose_name="Содержание")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def get_absolute_url(self):
        return reverse('answer', kwargs={'question_id': self.pk})

    def __str__(self):
        return f"Ответ на: {self.question.title}"


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Лайк вопроса"
        verbose_name_plural = "Лайки вопросов"
        constraints = [UniqueConstraint(name="unique_user_question_like", fields=["user", "question"])]

    def __str__(self):
        return f"Лайк вопроса от {self.user.username}"


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Лайк ответа"
        verbose_name_plural = "Лайки ответов"
        constraints = [UniqueConstraint(name="unique_user_answer_like", fields=["user", "answer"])]

    def __str__(self):
        return f"Лайк ответа от {self.user.username}"
