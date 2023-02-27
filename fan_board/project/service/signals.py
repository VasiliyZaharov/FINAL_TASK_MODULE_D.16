from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comments, Article

@receiver(post_save, sender=Comments)
def notify_user_post(sender, instance, created, **kwargs):
    if created:
        post_author = instance.article.author
        post_author.email_user(
            subject=f'Новый комментарий к вашему посту, заголовок: {instance.article.title}',
            message=instance.text,
        )
