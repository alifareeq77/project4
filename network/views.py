import json
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import MultipleObjectsReturned

from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .forms import *


# index--------------------------------------
def index(request):
    posts = Post.objects.order_by('date').reverse()
    return render(request, "network/index.html", context={
        'posts': posts
    })


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
    followers = Following.objects.filter(followed_user=profile.user.id).count()
    following = Following.objects.filter(followed_by=profile.user.id).count()
    posts_number = Post.objects.filter(profile=profile).count()
    posts = Post.objects.filter(profile=profile).order_by('date').reverse()
    # for other users----------------------------------------------------------------------------------
    is_following = Following.objects.filter(followed_user=profile.user.id, followed_by=request.user)

    # check if the user is followed
    def is_f(is_ff):
        if is_ff:
            return "unfollow"
        else:
            return "Follow"

    form = PostForm()

    if request.method == 'PUT':

        data = json.loads(request.body)
        if data.get('profile_user_id') is not None:
            try:
                exist = Following.objects.get(followed_by_id=request.user.id,
                                              followed_user_id=data.get('profile_user_id'))
                exist.delete()
                resp = {'statue': is_f(Following.objects.filter(followed_by_id=request.user.id))}
                return JsonResponse(data=resp, status=204)
            except Following.DoesNotExist:
                Following.objects.create(followed_by_id=request.user.id,
                                         followed_user_id=data.get('profile_user_id')).save()
                resp = {'statue': is_f(Following.objects.filter(followed_by_id=request.user.id))}
                return JsonResponse(data=resp, status=204)
    return render(request, 'network/profile_view.html', {
        'profile': profile,
        'followers': followers,
        'following': following,
        'posts_number': posts_number,
        'posts': posts,
        'form': form,
        'is_followed': is_f(is_following)
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
        post_database = Post.objects.get(id=post_id_)

        if request.user.id == post_database.profile.user.id:
            data = json.loads(request.body)
            if data.get('post') is not None:
                post_database.post = data.get('post')
                post_database.save()
                print('updated db')
                return JsonResponse(post_database.serialize(), status=204)
        else:
            return HttpResponse(status=304)
