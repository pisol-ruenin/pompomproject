from django.conf.urls import url, include
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
    url(r'^movie/$', views.AllMovieView.as_view(), name='all_movie'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^movie/(?P<pk>[0-9]+)/$',
        views.MovieView.as_view(), name='movie'),
    url(r'^profile/(?P<pk>[0-9]+)/update/$',
        views.UpdateProfile.as_view(), name='update_profile'),
    url(r'^movie/(?P<pk>[0-9]+)/add_review/$',
        views.CreateReview.as_view(), name='add_review'),
    url(r'^movie/(?P<pk>[0-9]+)/review/(?P<review_pk>[0-9]+)/$',
        views.ReviewlView.as_view(), name='review'),
    url(r'^movie/(?P<pk>[0-9]+)/review/(?P<review_pk>[0-9]+)/update/$',
        views.UpdateReview.as_view(), name='update_review'),
    url(r'^movie/(?P<pk>[0-9]+)/review/(?P<review_pk>[0-9]+)/delete/$',
        views.DeleteReview.as_view(), name='delete_review'),
    url(r'^movie/search/', views.MovieSearchView.as_view(), name='search_movie'),
    url(r'^movie/(?P<pk>[0-9]+)/calculate_rating/$',
        views.CalculateRatingDelete.as_view(), name='calculate_rating_delete'),
    url(r'^movie/(?P<pk>[0-9]+)/review/(?P<review_pk>[0-9]+)/calculate_rating/$',
        views.CalculateRating.as_view(), name='calculate_rating'),
    url(r'^reviewer_request/send/$', views.ReviewerRequestSend.as_view(),
        name='reviewer_request_send'),
    url(r'^reviewer_request/$', views.ReviewerRequestView.as_view(),
        name='reviewer_request'),
    url(r'^reviewer_request/(?P<pk>[0-9]+)/update/$', views.ReviewerRequestEdit.as_view(),
        name='reviewer_request_update'),
    url(r'^profile/(?P<pk>[0-9]+)/update_balance/$',
        views.UpdateBalance.as_view(), name='update_balance'),
    url(r'^look_profile/(?P<pk>[0-9]+)/$',
        views.LookProfile.as_view(), name='look_profile'),
]
