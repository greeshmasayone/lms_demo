from rest_framework import serializers
from .models import Topic, Quiz, Question, QuizAttempt, Choices, QuizResult
from usermanagement.models import User

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'pass_score', 'points']


class TopicSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.get_full_name')
    quizzes = QuizSerializer(read_only=True, source='get_quizzes')

    class Meta:
        model = Topic
        fields = ["id", "name", "created_by", "category", "content", "description", "image", "quizzes", "banner_image",
                  "video"]

    def create(self, validated_data):
        request = self.context.get('request')
        return Topic.objects.create(created_by=request.user, **validated_data)


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Choices
        fields = ['id', 'choice', 'question', 'is_correct']
        read_only_fields = ['question']


class QuestionsSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='get_choices')
    right_answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question', 'choices', 'right_answer', 'score']

    def get_right_answer(self, obj):
        right_answer = obj.get_choices.filter(
            is_correct=True).first()
        return right_answer.choice if right_answer else None

    def create(self, validated_data):
        choices = validated_data.pop('get_choices')
        question = Question.objects.create(**validated_data)
        for choice in choices:
            Choices.objects.create(**choice, question=question)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('get_choices')
        instance.question = validated_data.get("question", instance.question)
        instance.save()
        keep_choices = []
        for choice in choices:
            if "id" in choice.keys():
                if Choices.objects.filter(id=choice["id"]).exists():
                    c = Choices.objects.get(id=choice["id"])
                    c.choice = choice.get('choice', c.choice)
                    c.save()
                    keep_choices.append(c.id)
                else:
                    continue
            else:
                c = Choices.objects.create(**choice, question=instance)
                keep_choices.append(c.id)
        return instance


class ChoicesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Choices
        fields = ['id', 'choice', 'question']
        read_only_fields = ['question']


class AttemptSerializer(serializers.ModelSerializer):
    choices = ChoicesSerializer(many=True, source='get_choices')

    class Meta:
        model = Question
        fields = ['id', 'question', 'choices', 'score']


class CompletedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizResult
        fields = ['user_id']

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [ 'point', 'email', 'id']
