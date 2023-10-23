from django.db import models
from django.contrib.auth.models import User

class MusicFile(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    MUSIC_FILE_TYPES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music/')
    type = models.CharField(max_length=20, choices=MUSIC_FILE_TYPES, default=PUBLIC)
    allowed_users = models.ManyToManyField(User, related_name='allowed_music_files', blank=True)

    def __str__(self):
        return self.title

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = CustomUser.objects.create_user(email, email, password)
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # invalid email or password
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

from django.urls import reverse

class MusicFile(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    MUSIC_FILE_TYPES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music/')
    type = models.CharField(max_length=20, choices=MUSIC_FILE_TYPES, default=PUBLIC)
    allowed_users = models.ManyToManyField(CustomUser, related_name='allowed_music_files', blank=True)

    def __str__(self):
        return self.title

    def is_allowed(self, user):
        if self.type == MusicFile.PUBLIC:
            return True
        elif self.type == MusicFile.PRIVATE and user == self.user:
            return True
        elif self.type == MusicFile.PROTECTED and user in self.allowed_users.all():
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse('musicfile_detail', args=[str(self.id)])


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def home(request):
    music_files = MusicFile.objects.filter(user=request.user)
    allowed_music_files = MusicFile.objects.filter(type=MusicFile.PUBLIC) | request.user.allowed_music_files.all()
    return render(request, 'home.html', {'music_files': music_files, 'allowed_music_files': allowed_music_files})



