from django.shortcuts import render, redirect
from .forms import NepaliUserCreationForm, NepaliAuthenticationForm
from django.contrib.auth import login, logout
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = NepaliUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("posts:list")
    else:
        form = NepaliUserCreationForm()
    return render(request, 'users/register.html', { "form": form })


def login_view(request):
    if request.method == 'POST':
        form = NepaliAuthenticationForm(data= request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("posts:list")
        
    else:
        form = NepaliAuthenticationForm()
    return render(request, 'users/login.html', { "form": form })

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("posts:list")
    return render(request, 'users/logout.html')