from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Категория задания'
        verbose_name_plural = 'Категории заданий'

    def __str__(self):
        return self.title


class ToDo(models.Model):
    title = models.CharField('Название', max_length=500, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_complete = models.BooleanField('Завершено', default=False)
    description = models.TextField(default='')
    starts = models.DateTimeField(null=True)
    num_notifications = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    is_notifications = models.BooleanField('Присылать уведомления', default=False)
    tg_chat_id = models.IntegerField(null=True)
    time_before_notification = models.IntegerField(default=0)
    phone = models.IntegerField(default=88005553535)
    address = models.CharField(max_length=200, default="Bay Area, San Francisco, CA")
    image = models.ImageField(upload_to='images', default='images/default.jpg')

    def __str__(self):
        return str(self.user)


class RegisterForm(UserCreationForm):
    # fields = ("username", 'email')
    # field_classes = {"username": UsernameField}

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
