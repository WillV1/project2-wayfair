from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, Post, City
from .forms import ProfileForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

#-----------STATIC PAGES
def home(request):
    return render(request, 'home.html')

#----------SIGNUP USER
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('new_profile')
        else: 
            error_message = 'Invalid sign up - try again'
            form = UserCreationForm()
            context = {'form': form, 'error_message': error_message}
            return render(request, 'registration/signup.html',context)
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

#---------------- PROFILE

@login_required
def new_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            
            return redirect('user_profile', new_profile.id)
        else:
            return render(request, 'profile/new.html', {'form': form})
    else: 
        form = ProfileForm()
        context = {'form': form}
        return render(request, 'profile/new.html', context)

@login_required
def user_profile(request, profile_id):
    profile = Profile.objects.get(user = request.user)
    return render(request, 'profile/index.html', {'profile': profile})

@login_required
def profile(request):#also known as profile index
    print(request.user)
    profile = Profile.objects.get(user = request.user)
    posts = Post.objects.filter(profile=profile)
    context = {'profile': profile, 'posts':posts}
    return render(request,'profile/index.html', context)

@login_required
def edit_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            updated_profile = profile_form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
        context = {'form': form}
        return render(request, 'profile/edit.html', context)

#----------------POSTS

@login_required
def view_post(request, post_id):
    post = Post.objects.get(id=post_id)

    context = {'post': post}
    return render(request, 'post/show.html', context)

#---------------- CITIES

@login_required
def cities_index(request):
    cities = City.objects.all()
    context = {'cities': cities}
    return render(request, 'city/index.html', context)

@login_required
def view_city(request, city_id):
    city = City.objects.get(id=city_id)
    posts = Post.objects.all().order_by('-timestamp')
    context = {'city': city, 'posts': posts}
    return render(request, 'city/show.html', context)