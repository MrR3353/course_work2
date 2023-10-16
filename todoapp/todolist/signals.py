from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from todolist.models import Profile, Category


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
        category = Category(user=instance, title="Новые")
        category.save()
        category = Category(user=instance, title="Срочные")
        category.save()
        category = Category(user=instance, title="Выполненные")
        category.save()
        category = Category(user=instance, title="В работе")
        category.save()

