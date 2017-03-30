from django.views import generic
from .models import Movie, UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'review_movie/index.html'

    def get_queryset(self):
        return Movie.objects.all()


class ProfileView(generic.ListView):
    template_name = 'review_movie/profile.html'

    def get_queryset(self):
        return self.UserProfile


class AllMovieView(generic.ListView):
    template_name = 'review_movie/all_movie.html'

    def get_queryset(self):
        return Movie.objects.all()


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
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('review_movie:index')
        return render(request, self.template_name, {'form': form})
