from django.views import generic
from .models import Movie, UserProfile, Review
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'review_movie/index.html'
    context_object_name = "movie_list"

    def get_queryset(self):
        movie = Movie.objects.all()[::-1]
        return movie[:3] if len(movie) >= 3 else movie

class UpdateProfile(UpdateView):
    model = UserProfile
    fields = ['nickname', 'profile_img', 'job']


class CreateReview(CreateView):
    model = Review
    fields = ['review', 'score']


class UpdateReview(UpdateView):
    model = Review
    fields = ['review', 'score']


class DeleteReview(DeleteView):
    pass


class AllMovieView(generic.ListView):
    context_object_name = "movie_list"
    template_name = 'review_movie/all_movie.html'
    paginate_by = 9

    def get_queryset(self):
        movie = Movie.objects.all()[::-1]
        return movie


class MovieView(generic.DetailView):
    model = Movie
    template_name = 'review_movie/movie.html'

    def get_context_data(self, **kwargs):
        context = super(MovieView, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(movie=self.get_object())
        return context


class ProfileView(generic.View):
    template_name = 'review_movie/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class UserFormView(generic.View):
    form_class = UserForm
    template_name = 'review_movie/register.html'

    # blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user_profile = UserProfile()
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user_profile.user = user
            user_profile.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('review_movie:index')
        return render(request, self.template_name, {'form': form})
