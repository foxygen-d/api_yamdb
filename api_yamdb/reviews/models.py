from django.contrib.auth.models import Group, AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class User(AbstractUser):

    role = models.ForeignKey(
        Group,
        null=False,
        blank=False,
        to_field='name',
        choices=[
            ('user', 'User'),
            ('moderator', 'Moderator'),
            ('admin', 'Admin'),
        ],
        default='user',
        related_name='users',
        on_delete=models.SET_DEFAULT
    )
    bio = models.TextField(
        'Biography',
        null=True,
        blank=True
    )


class Review(models.Model):
    """Модель для отзывов."""
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
    )
    text = models.TextField('Текст отзыва', help_text='Новый отзыв')
    score = models.SmallIntegerField(
        validators=[
            MinValueValidator(1, 'Ниже 1 оценку произведению ставить нельзя!'),
            MaxValueValidator(10, 'Выше 10 оценку произведению ставить нельзя!')
            ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв на {self.title}, оценка: {self.score}'


class Comments(models.Model):
    """Модель для комментариев."""
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Произведение',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
    )
    text = models.TextField('Текст комментария', help_text='Новый комментарий')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий к произведению {self.title}'
