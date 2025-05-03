from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='xday_start'),
    path('quiz/', views.quiz, name='xday_quiz'),
    path('result/', views.result, name='xday_result'),
    path('history/', views.history, name='xday_history'),
    path('history/<int:session_id>/', views.history_detail, name='xday_history_detail'),
] 