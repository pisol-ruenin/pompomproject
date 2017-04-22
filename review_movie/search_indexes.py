from haystack import indexes

from .models import Movie


class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    released_date = indexes.DateField(model_attr='released_date')
    genre = indexes.CharField(model_attr='genre')
    director = indexes.CharField(model_attr='director')
    writer = indexes.CharField(model_attr='writer')
    film_production = indexes.CharField(model_attr='film_production')
    rating = indexes.FloatField(model_attr='rating')

    def get_model(self):
        return Movie

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
