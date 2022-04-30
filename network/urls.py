from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<int:user_id_>/", views.profile_view, name='profile_view'),
    # API routes
    path("edit_post/<int:post_id_>", views.edit_post, name='edit_post')
]
