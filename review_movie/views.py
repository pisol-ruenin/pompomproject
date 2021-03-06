from django.views.generic import DetailView, View, ListView
from .models import Movie, UserProfile, Review, ReviewerRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm, ReviewForm
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from haystack.generic_views import SearchView
from hitcount.views import HitCountDetailView, HitCountMixin


class IndexView(ListView):
    template_name = 'review_movie/index.html'
    context_object_name = "movie_list"

    def get_queryset(self):
        movie = Movie.objects.all()[::-1]
        return movie[:3] if len(movie) >= 3 else movie


class CreateReview(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'review_movie.add_review'
    template_name = 'review_movie/add_review.html'
    raise_exception = True
    model = Review
    form_class = ReviewForm
    # fields = ['topic', 'review', 'rating']

    def get_success_url(self, *args, **kwargs):
        return reverse('review_movie:calculate_rating', kwargs={'pk': self.kwargs['pk'], 'review_pk': self.object.pk})

    def dispatch(self, *args, **kwargs):
        try:
            review = Review.objects.filter(
                movie__pk=self.kwargs['pk']).get(reviewer=self.request.user)
            return HttpResponseRedirect(reverse('review_movie:movie', kwargs={'pk': self.kwargs['pk']}))
        except:
            return super(CreateReview, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        form.instance.movie = movie
        form.instance.reviewer = user
        return super(CreateReview, self).form_valid(form)


class UpdateReview(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'review_movie.change_review'
    template_name = 'review_movie/edit_review.html'
    raise_exception = True
    form_class = ReviewForm
    model = Review
    pk_url_kwarg = 'review_pk'
    #fields = ['topic', 'review', 'rating']

    def get_success_url(self, *args, **kwargs):
        return reverse('review_movie:calculate_rating', kwargs={'pk': self.kwargs['pk'], 'review_pk': self.kwargs['review_pk']})

    def dispatch(self, *args, **kwargs):
        review = Review.objects.get(pk=self.kwargs['review_pk'])
        if self.request.user != review.reviewer:
            return HttpResponseRedirect(reverse('review_movie:review', kwargs={'pk': self.kwargs['pk'], 'review_pk': self.kwargs['review_pk']}))
        return super(UpdateReview, self).dispatch(*args, **kwargs)


class DeleteReview(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'review_movie.delete_review'
    raise_exception = True
    model = Review

    def get_success_url(self, *args, **kwargs):
        return reverse('review_movie:calculate_rating_delete', kwargs={'pk': self.kwargs['review_pk']})

    def dispatch(self, *args, **kwargs):
        review = Review.objects.get(pk=self.kwargs['pk'])
        if self.request.user != review.reviewer:
            return HttpResponseRedirect(reverse('review_movie:review', kwargs={'pk': self.kwargs['pk'], 'review_pk': self.kwargs['review_pk']}))
        return super(DeleteReview, self).dispatch(*args, **kwargs)


class AllMovieView(ListView):
    context_object_name = "movie_list"
    template_name = 'review_movie/all_movie.html'
    paginate_by = 9

    def get_queryset(self):
        movie = Movie.objects.all()[::-1]
        return movie


class ReviewlView(HitCountDetailView):
    model = Review
    template_name = 'review_movie/review.html'
    pk_url_kwarg = 'review_pk'
    count_hit = True

    def dispatch(self, *args, **kwargs):
        review = self.get_object()
        print(review.hit_count.hits)
        return super(ReviewlView, self).dispatch(*args, **kwargs)


class MovieView(DetailView):
    model = Movie
    template_name = 'review_movie/movie.html'

    def get_context_data(self, **kwargs):
        context = super(MovieView, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(movie=self.get_object())
        try:
            reviewer = Review.objects.filter(
                movie=self.get_object()).get(reviewer=self.request.user)
            context['ck_review'] = True
        except:
            context['ck_review'] = False
        return context


class ProfileView(LoginRequiredMixin, View):
    template_name = 'review_movie/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class UpdateProfile(LoginRequiredMixin, UpdateView):
    template_name = 'review_movie/profile_update.html'
    raise_exception = True
    model = UserProfile
    fields = ['nickname', 'profile_img', 'job', 'description']

    def get_success_url(self, *args, **kwargs):
        return reverse('review_movie:profile')

    def dispatch(self, *args, **kwargs):
        user_profile = UserProfile.objects.get(pk=self.request.user.pk)
        if self.request.user.pk != user_profile.pk:
            return HttpResponseRedirect(reverse('review_movie:profile'))
        return super(UpdateProfile, self).dispatch(*args, **kwargs)


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


class CalculateRatingDelete(PermissionRequiredMixin, UpdateView):
    permission_required = ['review_movie.add_review',
                           'review_movie.change_review', 'review_movie.delete_review']
    model = Movie
    raise_exception = True
    template_name = "review_movie/calculate_rating.html"
    fields = []

    def dispatch(self, *args, **kwargs):
        movie = self.get_object()
        reviews = Review.objects.filter(movie=movie)
        rating = 0
        for review in reviews:
            rating += review.rating
        try:
            rating /= len(reviews)
        except ZeroDivisionError:
            rating = 0.0
        movie.rating = rating
        movie.save()
        return HttpResponseRedirect(reverse('review_movie:movie', kwargs={'pk': self.kwargs['pk']}))


class CalculateRating(PermissionRequiredMixin, UpdateView):
    permission_required = ['review_movie.add_review',
                           'review_movie.change_review', 'review_movie.delete_review']
    model = Movie
    raise_exception = True
    template_name = "review_movie/calculate_rating.html"
    fields = []

    def dispatch(self, *args, **kwargs):
        movie = self.get_object()
        reviews = Review.objects.filter(movie=movie)
        rating = 0
        for review in reviews:
            rating += review.rating
        try:
            rating /= len(reviews)
        except ZeroDivisionError:
            rating = 0.0
        movie.rating = rating
        movie.save()
        return HttpResponseRedirect(reverse('review_movie:review', kwargs={'pk': self.kwargs['pk'], 'review_pk': self.kwargs['review_pk']}))


class ReviewerRequestSend(LoginRequiredMixin, CreateView):
    template_name = 'review_movie/reviewer_request.html'
    raise_exception = True
    model = ReviewerRequest
    fields = ['topic', 'request']

    def get_success_url(self, *args, **kwargs):
        return reverse('review_movie:reviewer_request')

    def dispatch(self, *args, **kwargs):
        try:
            requested = ReviewerRequest.objects.get(user=self.request.user)
        except:
            return super(ReviewerRequestSend, self).dispatch(*args, **kwargs)
        if self.request.user == requested.user:
            return redirect('review_movie:reviewer_request')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.confirm = None
        return super(ReviewerRequestSend, self).form_valid(form)


class ReviewerRequestView(LoginRequiredMixin, ListView):
    template_name = 'review_movie/reviewer_request_view.html'
    raise_exception = True
    context_object_name = "reviewer_request"

    def get_queryset(self):
        reviewer_request = ReviewerRequest.objects.get(user=self.request.user)
        return reviewer_request

    def dispatch(self, *args, **kwargs):
        try:
            requested = ReviewerRequest.objects.get(user=self.request.user)
        except:
            return redirect('review_movie:index')
        return super(ReviewerRequestView, self).dispatch(*args, **kwargs)


class ReviewerRequestEdit(LoginRequiredMixin, UpdateView):
    template_name = 'review_movie/reviewer_request.html'
    model = ReviewerRequest
    raise_exception = True
    fields = ['topic', 'request']

    def get_success_url(self):
        return reverse('review_movie:reviewer_request')

    def dispatch(self, *args, **kwargs):
        reviewer_request = ReviewerRequest.objects.get(user=self.request.user)
        if reviewer_request.confirm is True:
            return redirect('review_movie:reviewer_request')
        elif self.request.user != reviewer_request.user:
            return redirect('review_movie:index')
        return super(ReviewerRequestEdit, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.confirm = None
        return super(ReviewerRequestEdit, self).form_valid(form)


class MovieSearchView(SearchView):
    template_name = 'search/search.html'


class UpdateBalance(LoginRequiredMixin, UpdateView):
    model = User
    raise_exception = True
    template_name = "review_movie/update_balance.html"
    fields = []

    def dispatch(self, *args, **kwargs):
        user = self.get_object()
        my_review = Review.objects.filter(reviewer=self.request.user)
        balance = 0
        for review in my_review:
            balance += review.hit_count.hits
        balance *= 0.01
        user.userprofile.balance = balance
        user.userprofile.save()
        return redirect('review_movie:profile')


class LookProfile(DetailView):
    template_name = "review_movie/look_profile.html"
    context_object_name = "profile"

    def get_queryset(self):
        look_user = User.objects.filter(pk=self.kwargs['pk'])
        return look_user
