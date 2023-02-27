from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from .serializers import TopicSerializer, QuizSerializer, QuestionsSerializer, AttemptSerializer, ChoiceSerializer,\
    CompletedUserSerializer
from .models import Topic, Quiz, Question, QuizAttempt, Choices, Category, QuizResult


class TopicView(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, ]
    search_fields = ['name', 'category', 'created_by_id', 'description']
    http_method_names = ['get', 'post', 'delete', 'put', 'patch']

    def get_queryset(self):
        queryset = Topic.objects.filter(created_by=self.request.user)
        return queryset


class QuizView(generics.ListCreateAPIView):
    def get_object(self):
        topic_pk = self.kwargs.get('topic_id')
        topic = get_object_or_404(Topic, id=topic_pk)
        return topic

    def post(self, request, *args, **kwargs):
        serializer = QuizSerializer(data=request.data)
        topic = self.get_object()
        if serializer.is_valid():
            serializer.save(topics=topic)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        topic_pk = self.kwargs.get('topic_id')
        queryset = Quiz.objects.filter(topics=topic_pk)
        serializer = QuizSerializer(queryset, many=True)
        return Response(serializer.data)


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = QuizSerializer

    def get_object(self):
        quiz_id = self.kwargs.get('quiz_pk')
        quiz = get_object_or_404(Quiz, id=quiz_id)
        return quiz


class ChoiceView(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, ]
    search_fields = ['id', 'question']
    http_method_names = ['get', 'post', 'delete', 'put', 'patch']

    def get_queryset(self):
        queryset = Choices.objects.all()
        return queryset


class QuestionView(generics.ListCreateAPIView):
    serializer_class = QuestionsSerializer
    queryset = Question.objects.all()

    def get_object(self):
        quiz_pk = self.kwargs.get('quiz_id')
        quiz = get_object_or_404(Quiz, id=quiz_pk)
        return quiz

    def post(self, request, *args, **kwargs):
        serializer = QuestionsSerializer(data=request.data)
        quiz = self.get_object()
        if serializer.is_valid():
            serializer.save(quiz=quiz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        quiz_pk = self.kwargs.get('quiz_id')
        queryset = Question.objects.filter(quiz=quiz_pk)
        serializer = QuestionsSerializer(queryset, many=True)
        return Response(serializer.data)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = QuestionsSerializer

    def get_object(self):
        question_id = self.kwargs.get('question_pk')
        question = get_object_or_404(Question, id=question_id)
        return question


class QuizAttemptView(generics.ListCreateAPIView):
    # serializer_class = AttemptSerializer

    def post(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=self.kwargs.get('quiz_id'))
        user = self.request.user
        questions = request.data['questions']
        user_score = total_mark = 0
        quiz_results = []
        for question in questions:
            question_obj = Question.objects.filter(id=question.get('question_id')).first()
            user_choice = question.get('answer')
            total_mark += question_obj.score
            choice = question_obj.get_choices.filter(is_correct=True).first()
            if user_choice == choice.id:
                is_right = True
                user_score += question_obj.score
                quiz_results.append({'question': question_obj.id, 'user_choice': user_choice, 'is_correct': is_right})
            else:
                is_right = False
                quiz_results.append({'question': question_obj.id, 'user_choice': user_choice, 'is_correct': is_right})
            answer = Choices.objects.get(id=user_choice)
            user_quiz, created = QuizResult.objects.get_or_create(user=user, quiz=quiz, user_score=user_score)
            user_quiz.user_choice = answer
            user_quiz.is_right = is_right
            highest_score = user_quiz.total_score
            try:
                percentage_value = user_score / total_mark
                percentage = round(percentage_value * 100)
                percentage = 100 if percentage > 100 else percentage
            except ZeroDivisionError:
                percentage = 0
            if percentage > highest_score:
                user_quiz.total_score = highest_score = percentage
            if percentage >= quiz.pass_score:
                user_quiz.has_passed = has_passed = True
            else:
                has_passed = False
            user_quiz.save()
        data = {'quiz': quiz_results, 'current_score': user_score, 'total_mark': total_mark,
                'highest_score': highest_score, 'has_passed': has_passed}
        return Response(data={'status': True, 'error': None, 'data': data}, status=HTTP_200_OK)


class CompletedUsersView(generics.ListAPIView):
    serializer_class = CompletedUserSerializer

    def get_queryset(self):
        queryset = QuizResult.objects.filter(has_passed=True)
        return queryset
