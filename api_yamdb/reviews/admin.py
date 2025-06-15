from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, TitleGenre


class TitleGenreTabular(admin.TabularInline):
    model = TitleGenre


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
        'get_genres',
    )
    list_editable = (
        'name',
        'year',
        'description',
        'category',
    )
    list_filter = (
        'year',
        'category',
    )
    search_fields = ('name',)
    inlines = (TitleGenreTabular,)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_editable = (
        'name',
        'slug',
    )
    search_fields = ('slug',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_editable = (
        'name',
        'slug',
    )
    search_fields = ('slug',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'score',
        'text',
        'author',
        'pub_date'
    )
    list_editable = (
        'score',
        'text',
    )
    list_filter = ('score',)
    search_fields = ('author__username',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    list_editable = (
        'text',
    )
    search_fields = ('author__username',)
