from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    empty_value_display = '-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title', 'text')
    empty_value_display = '-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year',
        'description', 'category', 'genre',
    )
    search_fields = ('name',)
    empty_value_display = '-'


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Title)
