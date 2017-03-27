from django.contrib import admin
from .models import Movie
from django.forms import Textarea, TextInput
from django.db import models

# Register your models here.


class MovieModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }
admin.site.register(Movie, MovieModelAdmin)
