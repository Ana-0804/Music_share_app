dump.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.create_user(username=email, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')

def custom_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')
