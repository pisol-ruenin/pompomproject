from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=100)
    synopsis = models.TextField(max_length=1000)
    released_date = models.DateField()
    movie_image = models.CharField(max_length=1000)
    genre = models.CharField(max_length=250)
    director = models.CharField(max_length=100)
    film_production = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' - ' + self.film_production


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=50)
    profile_img = models.ImageField(
        upload_to='review_movie/img/avatar', blank=True)


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)
    score = models.IntegerField()
    reviewer = models.CharField(max_length=100)
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.movie.name) + ' - ' + self.reviewer + ' #' + str(self.review_date)
