from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import DateBaseModel
from rest_framework.exceptions import ValidationError
from usermanagement.models import User


class Category(DateBaseModel):
    title = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), null=True, blank=True)


class Topic(DateBaseModel):
    name = models.CharField(_("Name"), max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Created By"),
                                   related_name='get_topic', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"),
                                 related_name='content_topic_listing')
    description = models.TextField(_("Description"), null=True, blank=True)
    content = models.TextField(_("Content"), null=True, blank=True)
    banner_image = models.ImageField(_("Banner Image"), upload_to='topic-images', null=True)
    image = models.ImageField(_("Topic Image"), null=True, blank=True, upload_to='topic_images')
    video = models.URLField(_("Video URL"), null=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.name


class Quiz(DateBaseModel):
    name = models.CharField(_("Name"), max_length=500)
    topics = models.OneToOneField(Topic, on_delete=models.CASCADE, related_name='get_quizzes', verbose_name=_("Topics"))
    description = models.TextField(_("Description"), null=True, blank=True)
    pass_score = models.PositiveSmallIntegerField(_("Pass Percentage"), null=True, validators=[MinValueValidator(10),
                                                                                               MaxValueValidator(
                                                                                                   100)], )
    display_question_number = models.PositiveSmallIntegerField(_("No.of Questions"), validators=[MinValueValidator(1)],
                                                               null=True, blank=True),
    is_active = models.BooleanField(_("Is Active"), default=True, )
    points = models.PositiveSmallIntegerField(_("Quiz Score"), null=True, validators=[MinValueValidator(10), MaxValueValidator(
                                                                                                   100)], )

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.name


class Question(DateBaseModel):
    question = models.CharField(_("Question"), max_length=500)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name=_("Quiz"), related_name='get_quiz_questions')
    score = models.PositiveSmallIntegerField(_("Score"), validators=[MinValueValidator(0)], null=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Quiz Questions"

    def __str__(self):
        return self.question


class Choices(DateBaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("Questions"),
                                 related_name='get_choices')
    choice = models.CharField(max_length=100)
    is_correct = models.BooleanField(_("Is Correct"), default=False, )

    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return self.choice


class QuizAttempt(DateBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Attempted By"), related_name='get_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name=_("Quiz"), related_name='get_result')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("Question"), related_name='get_questions')
    user_choice = models.ForeignKey(Choices, on_delete=models.CASCADE, verbose_name=_("User Choice"), related_name='get_quiz_answer', null=True)
    is_right = models.BooleanField(_("Is Right"), default=False, )

    class Meta:
        verbose_name = "Attempts"
        verbose_name_plural = "Attempts"

    # def __str__(self):
    #     return self.user


class QuizResult(DateBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"), related_name='get_user_quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name=_("Quiz"), related_name='get_quiz_results')
    total_score = models.PositiveSmallIntegerField(_("Total Score"), default=0,)
    user_score = models.PositiveSmallIntegerField(_("User Score"), validators=[MinValueValidator(0)], null=True)
    has_passed = models.BooleanField(_("Has Passed"), default=False)

    class Meta:
        verbose_name = "User Quiz Results"
        verbose_name_plural = "User Quiz Results"

    # def __str__(self):
    #     return self.quiz
