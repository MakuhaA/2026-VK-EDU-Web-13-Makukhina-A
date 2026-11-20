from django import forms
from django.contrib.auth import user_logged_in

from .models import Question, Answer, Tag, ImageModel
from django import forms


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        label="Теги",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите теги через запятую (например: python, django, web)'
        })
    )

    class Meta:
        model = Question
        fields = ('title', 'content', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок вопроса'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Текст вопроса'}),
        }

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]

        tags = []
        for name in tag_names:
            # Ищем тег в базе или создаем новый, если такого нет
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        return tags

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            if self.user:
                question.author = self.user
            question.save()
            question.tags.set(self.cleaned_data['tags'])
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите ваш ответ здесь...'
            }),
        }
        labels = {
            'content': ''
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = super().save(commit=False)
        if commit:
            answer.author = self.user
            answer.question = self.question
            answer.save()
        return answer


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ('title', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        image = super().save(commit=False)
        image.user = self._user
        answer.save()
        return answer
