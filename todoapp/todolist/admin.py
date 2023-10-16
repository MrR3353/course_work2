from django.contrib import admin

from .models import ToDo, Category, Profile

# Register your models here.
admin.site.register(Category)
admin.site.register(ToDo)
admin.site.register(Profile)