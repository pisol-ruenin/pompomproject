from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'review_movie'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'review_movie/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/review_movie'}, name='logout'),
    url(r'all_movie.html', views.AllMovieView.as_view(), name='all_movie')
]
