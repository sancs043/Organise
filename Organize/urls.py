"""Organize URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from boards import views

urlpatterns = [
    # map empty URL path to home view
    path('', views.home, name="Home"),
    # map /activities URL path to activities view
    path('activities/', views.activities, name='Activities'),

    # map /activity-details URL path to activityDetails view
    path('activity-details/', views.activityDetails, name='Activity Details'),

    # map /create-activity URL path to createActivity view
    path('create-activity/', views.createActivity, name='Create Activity'),

    # map /edit-activity URL path to editActivity view
    path('edit-activity/', views.editActivity, name='Edit Activity'),

    # map /my-activity URL path to myActivity view
    path('my-activity/', views.myActivity, name='My Activity'),

    # map /user-list URL path to userList view
    path('user-list/', views.userList, name='UserList'),

    # map /admin URL path to admin.site.urls
    path('admin/', admin.site.urls),

    # map /login URL path to login view
    path('login/', views.login, name='Login'),

    # map /register URL path to register view
    path('register/', views.register, name='Register'),

    # map /join-activity URL path to joinActivity view
    path('join-activity/', views.joinActiviy, name='JoinActivity'),

    # map /quit-activity URL path to quitActivity view
    path('quit-activity/', views.quitActivity, name="QuitActivity"),

    # map /delete-activity URL path to deleteActivity view
    path('delete-activity/', views.deleteActivity, name="DeleteActivity"),

    # map /upload-photo URL path to uploadPhoto view
    path('upload-photo/', views.uploadPhoto, name="UploadPhoto"),

    # map /user-profile URL path to userProfile view
    path('user-profile/', views.userProfile, name="UserProfile"),

    # map /follow URL path to follow view
    path('follow/', views.follow, name="Follow"),

    # map /unfollow URL path to unfollow view
    path('unfollow/', views.unfollow, name="UnFollow"),

    # map /logout URL path to logout view
    path('logout/', views.logout, name="Logout"),
]
