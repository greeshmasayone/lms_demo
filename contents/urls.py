from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from . import views
from .views import TopicView, QuizView, QuestionView, QuizDetail

router = DefaultRouter()
router.register('topics', TopicView, basename='topic')


urlpatterns = [
    path('topics/<int:topic_id>/quizzes/', views.QuizView.as_view()),
    path('quizzes/<int:quiz_pk>/', views.QuizDetail.as_view()),
    path('quizzes/<int:quiz_id>/questions/', views.QuestionView.as_view()),
    path('questions/<int:question_pk>/', views.QuestionDetail.as_view()),
    path('quizzes/<int:quiz_id>/attempt/', views.QuizAttemptView.as_view()),
    path('quizzes/completedusers/', views.CompletedUsersView.as_view()),
    path('quizzes/leadershipboard/', views.LeaderShipBoardView.as_view()),

]

urlpatterns += router.urls
