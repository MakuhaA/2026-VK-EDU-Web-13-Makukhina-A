from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import LoginForms, RegisterForm, ProfileForm
from .models import Profile


@login_required(login_url='/login')
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile_obj)

    return render(request, 'profile.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, 'reg.html', context={'form': form})


def login(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        form = LoginForms(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                next_url = request.POST.get('next') or next_url

                if next_url and url_has_allowed_host_and_scheme(
                        url=next_url,
                        allowed_hosts={request.get_host()},
                        require_https=request.is_secure()
                ):
                    return redirect(next_url)

                return HttpResponseRedirect(reverse('index'))
            else:
                form.add_error(None, 'Неверный логин или пароль')
    else:
        form = LoginForms()

    return render(request, 'login.html', context={'form': form, 'next': next_url})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))