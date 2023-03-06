from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError

from .models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class UserRegister(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password", "email"]

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        user = User.objects.create(**validated_data)

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        request = self.context.get('request')
        email = data['email']
        password = data['password']
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError(
                {'status': False,
                 'error': {'errorMessage': "Username does not exists"},
                 'data': {}}
            )
        if not password:
            raise serializers.ValidationError(
                {'status': False,
                 'error': {'errorMessage': "Enter password"},
                 'data': {}}
            )
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        email = validated_data['email']
        password = validated_data['password']
        user = authenticate(
            request=request, email=email, password=password)
        if not user:
            raise serializers.ValidationError(
                {'status': False,
                 'error': {
                     'errorMessage': "Username and password do not match"
                 },
                 'data': {}}
            )
        refresh = RefreshToken.for_user(user)
        data = {'refresh': str(refresh), 'access': str(refresh.access_token), 'username': user.username}

        return {'status': True, 'error': None, 'data': data}


class DetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_no", 'email', 'username']


class LogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad token')
