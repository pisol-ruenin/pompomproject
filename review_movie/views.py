from django.views import generic
from .models import Movie, UserProfile, Review
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm
from django.http import HttpRequest
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'review_movie/index.html'

    def get_queryset(self):
        return Movie.objects.all()


class UpdateProfile(UpdateView):
    model = UserProfile
    fields = ['nickname', 'profile_img', 'job']


class CreateReview(CreateView):
    model = Review
    fields = ['review', 'score']


class UpdateReview(UpdateProfile):
    model = Review
    fields = ['review', 'score']


class DeleteReview(DeleteView):
    pass


class ProfileView(generic.ListView):
    template_name = 'review_movie/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class AllMovieView(generic.ListView):
    template_name = 'review_movie/all_movie.html'

    def get_queryset(self):
        return Movie.objects.all()


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
