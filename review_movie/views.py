from django.views.generic import DetailView, View, ListView
from .models import Movie, UserProfile, Review
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
# Create your views here.


class IndexView(ListView):
    template_name = 'review_movie/index.html'
    context_object_name = "movie_list"

    def get_queryset(self):
        movie = Movie.objects.all()[::-1]
        return movie[:3] if len(movie) >= 3 else movie


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['firstname', 'lastname', 'nickname', 'profile_img', 'job']


class CreateReview(LoginRequiredMixin, CreateView):
    template_name = 'review_movie/add_review.html'
    model = Review
    fields = ['topic', 'review', 'rating']

    def form_valid(self, form):
        user = self.request.user
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        form.instance.movie = movie
        form.instance.reviewer = user
        return super(CreateReview, self).form_valid(form)


class UpdateReview(LoginRequiredMixin, UpdateView):
    template_name = 'review_movie/edit_review.html'
    model = Review
    pk_url_kwarg = 'review_pk'
    fields = ['topic', 'review', 'rating']


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('review_movie:index')


class AllMovieView(ListView):
    context_object_name = "movie_list"
    template_name = 'review_movie/all_movie.html'
    paginate_by = 9

    def get_queryset(self):
        movie = Movie.objects.all()[::-1]
        return movie


class ReviewView(DetailView):
    model = Review
    template_name = 'review_movie/review.html'
    pk_url_kwarg = 'review_pk'


class MovieView(DetailView):
    model = Movie
    template_name = 'review_movie/movie.html'

    def get_context_data(self, **kwargs):
        context = super(MovieView, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(movie=self.get_object())
        movie = self.get_object()
        context['rating'] = 0
        for review in context['reviews']:
            context['rating'] += review.rating
        try:
            context['rating'] /= len(context['reviews'])
        except ZeroDivisionError:
            context['rating'] = 0.0
        movie.rating = context['rating']
        movie.save()
        return context


class ProfileView(LoginRequiredMixin, View):
    template_name = 'review_movie/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class UserFormView(View):
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
