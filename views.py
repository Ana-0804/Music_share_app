from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import MusicFile

@login_required(login_url='/login/')
def home(request):
    music_files = MusicFile.objects.filter(models.Q(type='public') | models.Q(user=request.user) | models.Q(allowed_users=request.user))
    context = {
        'music_files': music_files,
    }
    return render(request, 'home.html', context)

@login_required(login_url='/login/')
def upload_music(request):
    if request.method == 'POST':
        form = MusicFileForm(request.POST, request.FILES)
        if form.is_valid():
            music_file = form.save(commit=False)
            music_file.user = request.user
            music_file.save()
            form.save_m2m()
            messages.success(request, 'Your music file has been uploaded successfully!')
            return redirect('home')
    else:
        form = MusicFileForm()
    context = {
        'form': form,
    }
    return render(request, 'upload_music.html', context)

@login_required(login_url='/login/')
def view_music(request, music_id):
    music_file = get_object_or_404(MusicFile, id=music_id)
    if music_file.type == 'public' or music_file.user == request.user or request.user in music_file.allowed_users.all():
        context = {
            'music_file': music_file,
        }
        return render(request, 'view_music.html', context)
    else:
        messages.warning(request, 'You do not have access to view this music file.')
        return redirect('home')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('login')

