from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
# Create your views here.
def register(response):
    if response.method =="POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('/login')
    else:
        form = RegisterForm()

    return render(response, 'register/register.html',{"form":form})