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

from boards import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('activities/', views.activities, name='Activities'),
    path('activity-details/', views.activityDetails, name='Activity Details'),
    path('create-activity/', views.createActivity, name='Create Activity'),
    path('edit-activity/', views.editActivity, name='Edit Activity'),
    path('my-activity/', views.myActivity, name='My Activity'),
    path('user-list/', views.userList, name='UserList'),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='Login'),
    path('register/', views.register, name='Register'),
    path('join-activity/', views.joinActiviy, name='JoinActivity'),
    path('quit-activity/', views.quitActivity, name="QuitActivity"),
    path('delete-activity/', views.deleteActivity, name="DeleteActivity"),
    path('upload-photo/', views.uploadPhoto, name="UploadPhoto"),
    path('user-profile/', views.userProfile, name="UserProfile"),
    path('follow/', views.follow, name="Follow"),
    path('unfollow/', views.unfollow, name="UnFollow"),
    path('logout/', views.logout, name="Logout")
]
