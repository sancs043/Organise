from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from boards.models import Activity, User2, UserActivity

from boards.forms import LoginForm, RegisterForm, CreateActivity, EditActivity

import datetime

def activities(request):
    activities = Activity.objects.all()
    userid = request.COOKIES['userid']
    if "email" in request.POST:
        email = request.POST.get()

    return render(request, 'activity.html', {'activities': activities, 'userid': userid})

def createActivity(request):

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
        context['form'] = CreateActivity()
        return render(request, 'createActivity.html', context)

def activityDetails(request):
    userid = request.COOKIES['userid']
    activityid = request.GET.get('activityid')
    activity = Activity.objects.get(id=activityid)

    isUserAlreadyJoined = UserActivity.objects.filter(user=userid, activity=activityid).exists()

    return render(request, 'activityDetails.html', {'activity': activity, 'isUserAlreadyJoined': isUserAlreadyJoined })

def myActivity(request):
    userid = request.COOKIES['userid']
    user_email = request.COOKIES['user_email']
    ownedActivities = Activity.objects.filter(creator=userid)
    joinedActivities = UserActivity.objects.filter(user=userid)

    return render(request, 'myActivity.html', {'ownedActivities': ownedActivities, 'joinedActivities': joinedActivities})

def users(request):
    users = User2.objects.all()
    return render(request, 'User.html', {'kullanicis': users})

def register(request):
    if "email" in request.POST:

        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("name")
        surname = request.POST.get("surname")

        try:

            user = User2.objects.get(email=email)
            return redirect('Register')

        except User2.DoesNotExist:

            user = User2(email=email, password=password, name=name, surname=surname)
            user.save()
            return redirect('Login')
    else:
        context = {}
        context['form'] = RegisterForm()
        return render(request, 'register.html', context)

def login(request):
    if "email" in request.POST:

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:

            user = User2.objects.get(email=email, password=password)
            response = redirect('Activities')
            response.set_cookie('userid', user.id)
            response.set_cookie('user_email', user.email)
            return response

        except User2.DoesNotExist:

            return redirect('Login')

    else:

        context = {}
        context['form'] = LoginForm()
        return render(request, 'login.html', context)

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
    activity_id = request.GET.get('activity')
    activity = Activity.objects.get(id=activity_id)

    if request.method == 'POST':
        form = EditActivity(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('/activity-details?activityid=' + str(activity.id))
    else:
        form = EditActivity(instance=activity)

    return render(request, 'edit-activity.html', {'form': form})



