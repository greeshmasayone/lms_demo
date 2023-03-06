from django.contrib import admin
from .models import Topic, Category, Quiz, Question, Choices, QuizAttempt, QuizResult


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "category", "created_by"]
    fields = ["name", "description", "category"]
    search_fields = ["id", "category", "name"]
    list_display_links = ["name"]


@admin.register(Category)
class CatAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "pk"]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'topics', 'pass_score', 'is_active', 'points']
    fields = ['name', 'topics', 'description', 'pass_score', 'is_active', 'points']
    search_fields = ['name', 'description', 'pass_score', 'topics']
    list_filter = ['is_active', 'topics']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'quiz', 'score']
    fields = ['question', 'quiz', 'score']
    search_fields = ['question', 'quiz__name', 'position', 'score']
    list_filter = ['quiz']


@admin.register(Choices)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'choice', 'is_correct']
    fields = ['question', 'choice', 'is_correct']
    search_fields = ['question', 'position']


@admin.register(QuizAttempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'quiz_id', 'user_choice', 'is_right']
    fields = ['question', 'quiz', 'user_choice', 'is_right']
    search_fields = ['question', 'quiz__name', 'position', 'choice']
    list_filter = ['quiz']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'total_score', 'user_score', 'has_passed']
    fields = ['user', 'quiz', 'total_score', 'user_score', 'has_passed']
    search_fields = ['user__email', 'quiz__name']
    list_filter = ['quiz', 'has_passed']
