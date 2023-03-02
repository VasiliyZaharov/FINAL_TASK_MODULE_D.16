from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse


class Article(models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('tank', 'Танки'),
        ('buyers', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('quest', 'Квестгилверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастер заклинаний'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    author_id = author.primary_key
    title = models.CharField(max_length=64, verbose_name='заголовок')
    text = models.CharField(max_length=64, verbose_name='текст')
    category = models.CharField(max_length=11, choices=TYPE, default='tank', verbose_name='категория')
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Статья № {self.pk}, Заголовок: {self.title}'

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.pk)])

    class Meta:
        verbose_name = 'статью'
        verbose_name_plural = 'Статьи'


# class StatusFilterComments(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status=False)

class Comments(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    time_in = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=64, verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Статус', default=False)
    # object = StatusFilterComments()

    class Meta:
        verbose_name='комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'Пользователь {self.author} написал: {self.text}'



