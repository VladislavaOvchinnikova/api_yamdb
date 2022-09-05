from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from api_yamdb.settings import ADDR_SENT_EMAIL
from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewset
from .permissions import (AdminOrReadOnly, IsAdminorReadOnly,
                          ReviewCommentPermission)
from .serializers import (APITokenObtainSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          TitleCreateUpdateSerializer, TitleSerializer,
                          UserSerializer, UserSerializerMe,
                          UserSerializerSignUp)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        """Переопределение метода получения queryset."""
        title = get_object_or_404(Title, pk=self.kwargs.get('titles_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Переопределение метода create."""
        title = get_object_or_404(Title, pk=self.kwargs.get('titles_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        """Переопределение метода получения queryset."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Переопределение метода create."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CustomTokenObtainPairView(TokenViewBase):
    """View-класс для токена"""
    serializer_class = APITokenObtainSerializer


class APISignUp(APIView):
    """View-функция для самостоятельной регистрации пользователя"""
    serializer_class = UserSerializerSignUp

    def send_code(self, user, email):
        """Генерация и отправка кода подтверждения"""
        token = default_token_generator.make_token(user)
        send_mail(
            'res',
            token,
            ADDR_SENT_EMAIL,
            [email]
        )

    def post(self, request):
        """Обработка post-запроса самостоятельной регистрации пользователя"""
        serializer = UserSerializerSignUp(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        is_registered = User.objects.filter(
            email=email, username=username)
        if not is_registered.exists():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            self.send_code(user, email)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = get_object_or_404(User, email=email, username=username)
            self.send_code(user, email)
            response = {
                'error': 'Пользователь уже зарегистрирован в системе!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """View-класс для модели Post."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get(self, request):
        """Получение/изменение данных текущего пользователя"""
        if request.method == 'GET':
            serializer = UserSerializer(request.user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializerMe(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        role = serializer.validated_data.get('role')
        if (
            request.method == 'PATCH'
            and request.user.is_user
            and role is not None
        ):
            serializer = UserSerializer(request.user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewset):
    """View-класс для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminorReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewset):
    """View-класс для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminorReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """View-класс для модели Title."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminorReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Переопределение метода получения сериализатора."""
        if self.action in ('create', 'partial_update',):
            return TitleCreateUpdateSerializer
        return TitleSerializer
