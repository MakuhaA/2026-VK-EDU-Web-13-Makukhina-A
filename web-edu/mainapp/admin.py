from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Question, Answer, Tag, QuestionLike, AnswerLike
from core.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ('author', 'content', 'is_correct')
    raw_id_fields = ('author',)


class MyFilter(admin.SimpleListFilter):
    title = "Автор"

    parameter_name = 'author_id'

    def lookups(self, request, model_admin):
        author_ids = Question.objects.values_list('author', flat=True).distinct()
        return [(str(author_id), f'{author_id}') for author_id in author_ids]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author_id=int(self.value()))
        return queryset


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'likes_count')
    list_filter = ('created_at', 'tags', MyFilter)
    search_fields = ('title',)
    inlines = [AnswerInline]

    raw_id_fields = ('author',)

    def likes_count(self, obj):
        return obj.question_likes.count()

    likes_count.short_description = 'Кол-во лайков'

@admin.register(Answer)
class Answer(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at')
    list_filter = ('author', 'question')
    search_fields = ('question', 'author')

    list_select_related = ('question', 'author')
    raw_id_fields = ('author',)


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(QuestionLike)
class QuestionLike(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'created_at')
    list_select_related = ('user', 'question')
    raw_id_fields = ('user', 'question')


@admin.register(AnswerLike)
class AnswerLike(admin.ModelAdmin):
    list_display = ('id', 'user', 'answer', 'created_at')
    list_select_related = ('user', 'answer')
    raw_id_fields = ('user', 'answer')
