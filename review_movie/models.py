from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=100)
    synopsis = models.TextField(max_length=1000)
    released_date = models.DateField()
    genre = models.CharField(max_length=250)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=200)
    film_production = models.CharField(max_length=100)
    movie_poster = models.ImageField()
    trailer_video = models.CharField(max_length=1000)
    rating = models.FloatField()

    def __str__(self):
        return self.name + ' - ' + self.film_production


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(
        max_length=20, blank=True)
    job = models.CharField(max_length=50, blank=True)
    profile_img = models.ImageField(
        default='default/defult_profile.png', blank=True)
    balance = models.FloatField(default=0)

    def __str__(self):
        return str(self.user)


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    review = models.TextField(max_length=8000)
    rating = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)])
    reviewer = models.ForeignKey(User, null=True)
    review_date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('review_movie:review', kwargs={'pk': self.movie.pk, 'review_pk': self.pk})

    def __str__(self):
        return str(self.movie.name) + ' - ' + str(self.reviewer) + ' #' + str(self.review_date)


class ReviewerRequest(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    topic = models.CharField(max_length=50)
    request = models.TextField(max_length=5000)
    request_date = models.DateField(auto_now_add=True)
    confirm = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('review_movie:request_view', kwargs={'pk': self.movie.pk, 'review_pk': self.pk})

    def __str__(self):
        return self.topic + ' ' + str(self.user)
