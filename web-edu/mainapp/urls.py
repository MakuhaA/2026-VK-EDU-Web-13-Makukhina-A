from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('profile/', views.profile, name='profile'),
    path('ask/', views.ask, name='ask'),
    path('answer/<int:question_id>/', views.answer, name='answer'),
    path('tag/<str:tag_name>/', views.questions_by_tag, name='tag_questions'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]