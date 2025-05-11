from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NepaliUserCreationForm, NepaliAuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = NepaliUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:login")
    else:
        form = NepaliUserCreationForm()
    return render(request, 'users/register.html', {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = NepaliAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("users:profile")
    else:
        form = NepaliAuthenticationForm()
    return render(request, 'users/login.html', {"form": form})

@login_required(login_url="/users/login/")
def profile_view(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("/")
    return render(request, 'users/logout.html')