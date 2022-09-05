from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializerSignUp(serializers.ModelSerializer):
    """Сериализатор для модели User для самостоятельной регистрации"""

    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )

    def validate(self, attrs):
        errors = []
        username = attrs.get('username')
        if username.lower() == 'me':
            errors.append('Нельзя зарегистрировать с username=me!')
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserSerializerMe(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class APITokenObtainSerializer(serializers.Serializer):
    """Сериализатор для токена"""

    @classmethod
    def get_token(cls, user):
        """Генерация токена"""
        return RefreshToken.for_user(user).access_token

    def validate(self, attrs):
        """Валидация кода подтверждения и выдача токена"""
        request = self.context.get('request')
        authenticate_kwargs = {
            'request': request,
            'username': request.data.get('username'),
            'confirmation_code': request.data.get('confirmation_code'),
        }
        if request.data.get('username') is None:
            raise serializers.ValidationError('Необходимо указать username')
        user = get_object_or_404(User, username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')
        res = default_token_generator.check_token(user, confirmation_code)
        if not res:
            raise serializers.ValidationError('Неверный код подтверждения')
        self.user = authenticate(**authenticate_kwargs)
        return {'token': str(self.get_token(user))}


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title = self.context['view'].kwargs.get('titles_id')
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title, author=user).exists():
                raise serializers.ValidationError(
                    'Можно оставить только 1 отзыв на произведение.'
                )
        return data


class TitleSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=None, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleCreateUpdateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'
