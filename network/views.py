import json
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import MultipleObjectsReturned
from django.core.serializers import serialize
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .forms import *


# index--------------------------------------
def index(request):
    return render(request, "network/index.html")


# login--------------------------------------------------
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# register---------------------------------------------------------------
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        try:
            Profile.objects.create(user=user).save()
        except MultipleObjectsReturned:
            return render(request, "network/register.html", {
                "message": "smth with creating profile"
            })

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# profile view---------------------------------------------------------------------------------------------------------
def profile_view(request, user_id_):  # profile view function
    profile = Profile.objects.get(user_id=user_id_)
    followers = Profile.objects.get(user_id=user_id_).follower.count()
    following = Profile.objects.get(user_id=user_id_).following.count()
    posts_number = Post.objects.filter(profile=profile).count()
    posts = Post.objects.filter(profile=profile)

    form = PostForm()
    return render(request, 'network/profile_view.html', {
        'profile': profile,
        'followers': followers,
        'following': following,
        'posts_number': posts_number,
        'posts': posts,
        'form': form
    })


# create post --------------------------------------------------------------------------
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            post = form.cleaned_data['post']
            user_name = request.user
            user = User.objects.get(username=user_name)
            profile = Profile.objects.get(user=user)
            Post.objects.create(post=post, profile=profile).save()

    return redirect('profile_view', request.user.id)


# handling the put request of editing post -------------------------------------------------------
def edit_post(request, post_id_):
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('post') is not None:
            post_database = Post.objects.get(id=post_id_)
            post_database.post = data.get('post')
            post_database.save()
            print('updated db')
            return JsonResponse(post_database.serialize(), status=204)
