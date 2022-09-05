from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import validate_year

MAX_SCORE = 10
MIN_SCORE = 1


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Название страницы'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Название страницы'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Category,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                MAX_SCORE, f'Поставьте оценку от {MIN_SCORE} до {MAX_SCORE}'),
            MinValueValidator(
                MIN_SCORE, f'Поставьте оценку от {MIN_SCORE} до {MAX_SCORE}')
        ],
        verbose_name="Рейтинг"
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author'
            )
        ]

    def __str__(self):
        return f"{self.title} - {self.text[:30]}"


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Обзор',
        related_name='comments'
    )
    text = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    pub_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:30]
