from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('ask/', views.ask, name='ask'),
    path('answer/<int:question_id>/', views.answer, name='answer'),
    path('tag/<str:tag_name>/', views.questions_by_tag, name='tag_questions'),
    path('ajax/like/question/<int:question_id>/', views.like_question_async, name='like_question_async'),
    path('ajax/like/answer/<int:answer_id>/', views.like_answer_async, name='like_answer_async'),
    path('ajax/mark-correct/<int:question_id>/<int:answer_id>/', views.mark_correct_answer, name='mark_correct_answer'),
]
