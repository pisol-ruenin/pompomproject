from django.contrib import admin
from .models import Movie
from .models import Review
from django.forms import Textarea, TextInput
from django.db import models

# Register your models here.


class MovieModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }


class ReviewModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 80})}
    }

admin.site.register(Movie, MovieModelAdmin)
admin.site.register(Review, ReviewModelAdmin)
