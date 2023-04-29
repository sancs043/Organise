from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from boards.models import Activity, User2, UserActivity, UserFollowings

from boards.forms import LoginForm, RegisterForm, CreateActivityForm
from boards.forms import EditActivityForm, UploadPhotoForm, UserPhotos

import datetime
import hashlib

from boards.mailSender import sendEmail

def home(request):

    try:
        userid = request.COOKIES['userid']
    except Exception as e:
        print(e)
        return redirect('Login')

    posts = UserPhotos.objects.all()

    return render(request, 'home.html', {'userid': userid, 'posts': posts })


def activities(request):

    try:
        userid = request.COOKIES['userid']
    except Exception as e:
        print(e)
        return redirect('Login')

    activities = Activity.objects.all()
    posts = UserPhotos.objects.all()

    if "email" in request.POST:
        email = request.POST.get()

    return render(request, 'activity.html', {'activities': activities, 'userid': userid, 'posts': posts })

def createActivity(request):

    userid = request.COOKIES['userid']

    if "name" in request.POST:

        description = request.POST.get("description")
        maxPeople = request.POST.get("maxPeople")
        name = request.POST.get("name")
        date_day = int(request.POST.get("date_day"))
        date_month = int(request.POST.get("date_month"))
        date_year = int(request.POST.get("date_year"))
        location = request.POST.get("location")

        if description == '': #above are empty redirect to createactivity
            return redirect('CreateActivity')
        else:
            userid = request.COOKIES['userid']
            user = User2.objects.get(id=userid)

            date = datetime.date(date_year, date_month, date_day)
            activity = Activity(name=name, description=description, maxPeople= maxPeople, date = date, location= location, creator= user)
            activity.save()
            return redirect('Activities')
    else:
        context = {}
        context['form'] = CreateActivityForm()
        context['userid'] = userid
        return render(request, 'createActivity.html', context)

def activityDetails(request):
    userid = request.COOKIES['userid']
    activityid = request.GET.get('activityid')
    activity = Activity.objects.get(id=activityid)

    isUserAlreadyJoined = UserActivity.objects.filter(user=userid, activity=activityid).exists()

    return render(request, 'activityDetails.html', {'userid': userid, 'activity': activity, 'isUserAlreadyJoined': isUserAlreadyJoined })

def myActivity(request):
    userid = request.COOKIES['userid']
    user_email = request.COOKIES['user_email']
    ownedActivities = Activity.objects.filter(creator=userid)
    joinedActivities = UserActivity.objects.filter(user=userid)

    return render(request, 'myActivity.html', {'userid': userid, 'ownedActivities': ownedActivities, 'joinedActivities': joinedActivities})

def userList(request):

    followerId = request.GET.get('followerId')
    followingId = request.GET.get('followingId')
    search = request.GET.get('search')

    users = None

    if search:
        users = User2.objects.all()

    elif followingId:
        followingUser = User2.objects.get(id=followingId)
        followers = UserFollowings.objects.filter(following=followingUser)

        users = followers

    elif followerId:
        followerUser = User2.objects.get(id=followerId)
        followings = UserFollowings.objects.filter(follower=followerUser)

        users = followings

    return render(request, 'userList.html', {'userList': users, 'search': search, 'followingId': followingId, 'followerId': followerId})

def register(request):

    if "email" in request.POST:

        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("name")
        surname = request.POST.get("surname")

        password = hashlib.sha256(password.encode()).hexdigest()

        try:

            user = User2.objects.get(email=email)
            return redirect('Register')

        except User2.DoesNotExist:

            user = User2(email=email, password=password, name=name, surname=surname)
            user.save()

            sendEmail("Welcome to Organise", "Hi, you've successfully registered the Organise. Thanks", email)

            return redirect('Login')
    else:
        context = {}
        context['form'] = RegisterForm()
        return render(request, 'register.html', context)

def login(request):

    if "email" in request.POST:

        email = request.POST.get("email")
        password = request.POST.get("password")

        password = hashlib.sha256(password.encode()).hexdigest()

        try:

            user = User2.objects.get(email=email, password=password)
            response = redirect('Home')
            response.set_cookie('userid', user.id)
            response.set_cookie('user_email', user.email)
            return response

        except User2.DoesNotExist:

            return redirect('Login')

    else:

        context = {}
        context['form'] = LoginForm()
        return render(request, 'login.html', context)

def logout(request):

    response = redirect('Activities')
    response.delete_cookie('userid')
    response.delete_cookie('user_email')

    return response

def joinActiviy(request):

    userid = request.COOKIES['userid']
    activityid = request.GET.get('activityid')

    user = User2.objects.get(id=userid)
    activity = Activity.objects.get(id=activityid)

    user = UserActivity(user=user, activity=activity)
    user.save()

    return redirect('My Activity')

def deleteActivity(request):

    activityid = request.GET.get('activityid')

    activity = Activity.objects.get(id=activityid)
    activity.delete()

    return redirect('My Activity')

def editActivity(request):

    userid = request.COOKIES['userid']

    activity_id = request.GET.get('activityid')
    activity = Activity.objects.get(id=activity_id)

    if request.method == 'POST':

        if "name" in request.POST:

            description = request.POST.get("description")
            maxPeople = request.POST.get("maxPeople")
            name = request.POST.get("name")
            date_day = int(request.POST.get("date_day"))
            date_month = int(request.POST.get("date_month"))
            date_year = int(request.POST.get("date_year"))
            location = request.POST.get("location")

            if description == '': #above are empty redirect to createactivity
                return redirect('Activities')
            else:

                date = datetime.date(date_year, date_month, date_day)

                activity.name = name
                activity.description = description
                activity.maxPeople = maxPeople
                activity.date = date
                activity.location = location

                activity.save()

                return redirect('Activities')

    else:

        context = {}

        initial = {
            'name': activity.name,
            'description': activity.description,
            'date': activity.date,
            'maxPeople': activity.maxPeople,
            'location': activity.location
        }

        context['form'] = EditActivityForm(initial=initial)
        context['userid'] = userid
        return render(request, 'editActivity.html', context)

def quitActivity(request):

    userid = request.COOKIES['userid']
    activityid = request.GET.get('activityid')

    user = User2.objects.get(id=userid)
    activity = Activity.objects.get(id=activityid)

    userActivity = UserActivity.objects.get(user=user, activity=activity)
    userActivity.delete()

    return redirect('My Activity')

def uploadPhoto(request):

    if request.method == "POST":

        activityid = request.POST.get("activity")

        if activityid == '': #above are empty redirect to uploadPhoto
            return redirect('UploadPhoto')

        activity = Activity.objects.get(id=activityid)

        userid = request.COOKIES['userid']
        user = User2.objects.get(id=userid)

        photo = request.FILES.get('photo')

        date = datetime.datetime.now()

        userPhoto = UserPhotos(user=user, activity=activity, photo=photo, date=date)
        userPhoto.save()

        return redirect('Activities')

    else:
        context = {}

        userid = request.COOKIES['userid']
        user = User2.objects.get(id=userid)

        context['form'] = UploadPhotoForm(user)
        return render(request, 'uploadPhoto.html', context)

def userProfile(request):

    userid = request.COOKIES['userid']
    profileUserId = request.GET.get('userid')

    if not profileUserId:
        return redirect('Home')

    else:
        user = User2.objects.get(id=userid)
        profileUser = User2.objects.get(id=profileUserId)
        profileUserPosts = UserPhotos.objects.filter(user=profileUser)

        isFollowing = UserFollowings.objects.filter(follower=user, following=profileUser).exists()

        data = {'user': user, 'profileUser': profileUser, 'profileUserPosts': profileUserPosts, 'isFollowing': isFollowing }

        return render(request, 'userProfile.html', data)

def follow(request):

    followerId = request.GET.get('followerId')
    followingId = request.GET.get('followingId')

    followerUser = User2.objects.get(id=followerId)
    followingUser = User2.objects.get(id=followingId)


    userFollowing = UserFollowings(follower=followerUser, following=followingUser)
    userFollowing.save()

    return redirect('/user-profile?userid=' + followingId)

def unfollow(request):

    followerId = request.GET.get('followerId')
    followingId = request.GET.get('followingId')

    followerUser = User2.objects.get(id=followerId)
    followingUser = User2.objects.get(id=followingId)

    userFollowing = UserFollowings.objects.get(follower=followerUser, following=followingUser)
    userFollowing.delete()

    return redirect('/user-profile?userid=' + followingId)

