from django.shortcuts import render

# Create your views here.
# Import required modules

# This function deletes an activity
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from boards.models import Activity, User2, UserActivity, UserFollowings
from boards.forms import LoginForm, RegisterForm, CreateActivityForm
from boards.forms import EditActivityForm, UploadPhotoForm, UserPhotos
import datetime
import hashlib
from boards.mailSender import sendEmail
from django.contrib import messages
from django.db.models import Q


# Define the view for the homepage
def home(request):
    try:
        # Attempt to retrieve user ID from cookies
        userid = request.COOKIES['userid']
    except KeyError:
        # If there is an error retrieving the ID, redirect to login page
        return redirect('Login')

    # Retrieve the current user's follower ID
    follower = User2.objects.filter(id=userid).first()

    # Retrieve all UserPhotos objects from accounts the current user follows
    following_posts = UserFollowings.objects.filter(follower=follower)
    posts = UserPhotos.objects.filter(user__in=following_posts.values('following'))

    # Render the 'home.html' template and pass in the user ID and posts as context variables
    return render(request, 'home.html', {'userid': userid, 'posts': posts })

# Define the view for the 'activities' page
def activities(request):
    try:
        # Attempt to retrieve user ID from cookies
        userid = request.COOKIES['userid']
    except Exception as e:
        # If there is an error retrieving the ID, redirect to login page
        print(e)
        return redirect('Login')

    # Retrieve all Activity and UserPhotos objects
    activities = Activity.objects.all()

    # Retrieve creator's name for each activity
    creators = {}
    for activity in activities:
        creator = activity.creator
        creator_name = f"{creator.name} {creator.surname}"
        creators[activity.id] = creator_name

    posts = UserPhotos.objects.all()

    if "email" in request.POST:
        # Retrieve email from form if present
        email = request.POST.get()

    # Render the 'activity.html' template and pass in the activities, user ID, posts, and creators as context variables
    return render(request, 'activity.html',
                  {'activities': activities, 'userid': userid, 'posts': posts, 'creators': creators})


# Define the view for creating a new activity
def createActivity(request):

    try:
        # Retrieve user ID from cookies
        userid = request.COOKIES['userid']
    except Exception as e:
        return redirect('Login')

    if "name" in request.POST:
        # If form has been submitted, retrieve form data
        description = request.POST.get("description")
        maxPeople = request.POST.get("maxPeople")
        name = request.POST.get("name")
        date_day = int(request.POST.get("date_day"))
        date_month = int(request.POST.get("date_month"))
        date_year = int(request.POST.get("date_year"))
        location = request.POST.get("location")

        if description == '': #above are empty redirect to createactivity
            # If the description is empty, redirect to the create activity page
            return redirect('CreateActivity')
        else:
            # Otherwise, retrieve user information and create a new Activity object
            userid = request.COOKIES['userid']
            user = User2.objects.get(id=userid)

            date = datetime.date(date_year, date_month, date_day)
            activity = Activity(name=name, description=description, maxPeople= maxPeople, date = date, location= location, creator= user)
            activity.save()
            # Redirect to the 'activities' page
            return redirect('Activities')
    else:
        # If no form has been submitted, render the 'createActivity.html' template with an empty form and the user ID as context variables
        context = {}
        context['form'] = CreateActivityForm()
        context['userid'] = userid
        return render(request, 'createActivity.html', context)

# Define a function named "activityDetails" which accepts a request object
def activityDetails(request):
    # get the user ID from the cookies stored in the request object
    try:
        # Retrieve user ID from cookies
        userid = request.COOKIES['userid']
    except Exception as e:
        return redirect('Login')

    # get the activity ID from the GET parameters stored in the request object
    activityid = request.GET.get('activityid')
    # retrieve the activity object associated with the given activity ID
    activity = Activity.objects.get(id=activityid)

    maxPeopleReached = False
    userInActivity = UserActivity.objects.filter(activity=activityid).count()

    if userInActivity >= activity.maxPeople:
        maxPeopleReached = True

    # check if the user has already joined the activity
    isUserAlreadyJoined = UserActivity.objects.filter(user=userid, activity=activityid).exists()

    # render the activity details page with the user ID, activity details, and a flag indicating if the user has already joined the activity
    data = {'userid': userid, 'activity': activity, 'isUserAlreadyJoined': isUserAlreadyJoined, 'maxPeopleReached': maxPeopleReached }
    return render(request, 'activityDetails.html', data)

# Define a function named "myActivity" which accepts a request object
def myActivity(request):
    # get the user ID and user email from the cookies stored in the request object
    try:
        # Retrieve user ID from cookies
        userid = request.COOKIES['userid']
    except Exception as e:
        return redirect('Login')

    user_email = request.COOKIES['user_email']
    # retrieve the activities owned by the user
    ownedActivities = Activity.objects.filter(creator=userid)
    # retrieve the activities joined by the user
    joinedActivities = UserActivity.objects.filter(user=userid)

    # render the user's activity page with the user ID, owned activities, and joined activities
    return render(request, 'myActivity.html', {'userid': userid, 'ownedActivities': ownedActivities, 'joinedActivities': joinedActivities})

# Define a function named "userList" which accepts a request object
def userList(request):

    try:
        # Retrieve user ID from cookies
        userid = request.COOKIES['userid']
    except Exception as e:
        return redirect('Login')

    # get the follower ID, following ID, and search string from the GET parameters stored in the request object
    followerId = request.GET.get('followerId')
    followingId = request.GET.get('followingId')
    search = request.GET.get('search')

    # initialize the user list to None
    users = None

    # if the search string is not None, retrieve all user objects
    if search:
        users = User2.objects.filter(Q(name__contains=search) | Q(surname__contains=search) | Q(email__contains=search))

    # if the following ID is not None, retrieve all users who are following the user with the given following ID
    elif followingId:
        followingUser = User2.objects.get(id=followingId)
        followers = UserFollowings.objects.filter(following=followingUser)

        users = followers

    # if the follower ID is not None, retrieve all users who are followed by the user with the given follower ID
    elif followerId:
        followerUser = User2.objects.get(id=followerId)
        followings = UserFollowings.objects.filter(follower=followerUser)

        users = followings

    # render the user list page with the user list, search string, follower ID, and following ID
    return render(request, 'userList.html', {'userList': users, 'search': search, 'followingId': followingId, 'followerId': followerId})


# This function registers a new user to the system
def register(request):

    # check if a POST request containing email has been sent
    if "email" in request.POST:
        # retrieve the email, password, name, and surname from the request
        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("name")
        surname = request.POST.get("surname")

        if not email:
            messages.error(request, 'Please fill the required fields!')

        if not password:
            messages.error(request, 'Please fill the required fields!')

        if not name:
            messages.error(request, 'Please fill the required fields!')

        if not surname:
            messages.error(request, 'Please fill the required fields!')

        if not email or not password or not name or not surname:
            return redirect('Register')

        # hash the password using SHA-256 algorithm
        password = hashlib.sha256(password.encode()).hexdigest()

        try:
            # check if a user with the same email already exists
            user = User2.objects.get(email=email)
            # redirect to the registration page if the user already exists

            messages.error(request, 'A user has already registered with this email!')

            return redirect('Register')

        except User2.DoesNotExist:
            # create a new user with the provided email, password, name, and surname
            user = User2(email=email, password=password, name=name, surname=surname)
            # save the user to the database
            user.save()

            # send a welcome email to the new user
            sendEmail("Welcome to Organise", "Hi, you've successfully registered to Organise. Thanks", email)

            # redirect the user to the login page after successful registration
            return redirect('Login')
    else:
        # create an empty context dictionary
        context = {}
        # create a new RegisterForm object and assign it to the 'form' key in the context dictionary
        context['form'] = RegisterForm()
        # render the 'register.html' template with the context dictionary
        return render(request, 'register.html', context)


# This function logs in an existing user to the system
def login(request):
    # check if a POST request containing email has been sent
    if "email" in request.POST:
        # retrieve the email and password from the request
        email = request.POST.get("email")
        password = request.POST.get("password")

        # hash the password using SHA-256 algorithm
        password = hashlib.sha256(password.encode()).hexdigest()

        try:
            # retrieve the user with the provided email and password
            user = User2.objects.get(email=email, password=password)
            # redirect the user to the homepage after successful login
            response = redirect('Home')
            # set the 'userid' and 'user_email' cookies in the response object
            response.set_cookie('userid', user.id)
            response.set_cookie('user_email', user.email)
            return response

        except User2.DoesNotExist:
            # redirect the user to the login page if the provided email and password are incorrect
            return redirect('Login')

    else:
        # create an empty context dictionary
        context = {}
        # create a new LoginForm object and assign it to the 'form' key in the context dictionary
        context['form'] = LoginForm()
        # render the 'login.html' template with the context dictionary
        return render(request, 'login.html', context)
def logout(request):

    # redirect the user to the 'Activities' page
    response = redirect('Activities')
    # delete the 'userid' and 'user_email' cookies from the response object
    response.delete_cookie('userid')
    response.delete_cookie('user_email')
    # return the modified response object
    return response

# This function joins the user to an activity
def joinActiviy(request):
    # Get the user id from the cookie
    try:
        # Retrieve user ID from cookies
        userid = request.COOKIES['userid']
    except Exception as e:
        return redirect('Login')

    # Get the activity id from the GET request
    activityid = request.GET.get('activityid')

    # Get the user and activity objects from their respective models using their ids
    user = User2.objects.get(id=userid)
    activity = Activity.objects.get(id=activityid)

    # Create a new UserActivity object and save it to the database
    user = UserActivity(user=user, activity=activity)
    user.save()

    # Redirect the user to the 'My Activity' page
    return redirect('My Activity')

def deleteActivity(request):
    # Get the activity id from the GET request
    activityid = request.GET.get('activityid')

    # Get the activity object from the Activity model using its id
    activity = Activity.objects.get(id=activityid)

    # Get the list of users who joined the activity
    user_activity_list = UserActivity.objects.filter(activity=activity)

    # Send email to every user who joined the activity
    for user_activity in user_activity_list:
        user = user_activity.user
        subject = f"Activity {activity.name} has been deleted"
        message = f"Dear {user.name},\n\nThe activity '{activity.name}' that you joined has been deleted.\n\nBest regards,\nThe Activity Manager"
        send_mail(subject, message, 'admin@example.com', [user.email])

    # Delete the activity object
    activity.delete()

    # Redirect the user to the 'My Activity' page
    return redirect('My Activity')

def editActivity(request):  # defining a function to edit an activity

    # getting the userid from the request cookies
    try:
        # Retrieve user ID from cookies
        userid = request.COOKIES['userid']
    except Exception as e:
        return redirect('Login')


    activity_id = request.GET.get('activityid')  # getting the activityid from the GET request
    activity = Activity.objects.get(id=activity_id)  # getting the activity object with the activityid

    if request.method == 'POST':  # if the request method is POST

        if "name" in request.POST:  # if the name field is present in the POST request

            description = request.POST.get("description")  # getting the description from the POST request
            maxPeople = request.POST.get("maxPeople")  # getting the maxPeople from the POST request
            name = request.POST.get("name")  # getting the name from the POST request
            date_day = int(request.POST.get(
                "date_day"))  # getting the day of the date from the POST request and converting it to an integer
            date_month = int(request.POST.get(
                "date_month"))  # getting the month of the date from the POST request and converting it to an integer
            date_year = int(request.POST.get(
                "date_year"))  # getting the year of the date from the POST request and converting it to an integer
            location = request.POST.get("location")  # getting the location from the POST request

            if description == '':  # if the description is empty, redirect to the Activities page
                return redirect('Activities')
            else:
                date = datetime.date(date_year, date_month,
                                     date_day)  # creating a date object with the date components from the POST request

                activity.name = name  # setting the name of the activity object to the name from the POST request
                activity.description = description  # setting the description of the activity object to the description from the POST request
                activity.maxPeople = maxPeople  # setting the maxPeople of the activity object to the maxPeople from the POST request
                activity.date = date  # setting the date of the activity object to the date from the POST request
                activity.location = location  # setting the location of the activity object to the location from the POST request

                activity.save()  # saving the changes made to the activity object
                # send email to users who have joined the activity
                joined_users = activity.useractivity_set.all().values_list('user__email', flat=True)
                subject = f'Activity "{activity.name}" has been updated'
                message = f'Hi,\n\nThe activity "{activity.name}" has been updated. Please check the details on the website.\n\nBest,\nThe Team'
                send_mail(subject, message, 'from@example.com', joined_users, fail_silently=False)

                return redirect('Activities')  # redirecting to the Activities page

    else:  # if the request method is not POST

        context = {}  # creating an empty context dictionary

        initial = {  # creating a dictionary with initial values for the form
            'name': activity.name,
            'description': activity.description,
            'date': activity.date,
            'maxPeople': activity.maxPeople,
            'location': activity.location
        }

        context['form'] = EditActivityForm(
            initial=initial)  # adding the EditActivityForm with the initial values to the context dictionary
        context['userid'] = userid  # adding the userid to the context dictionary
        return render(request, 'editActivity.html',
                      context)  # rendering the editActivity.html page with the context dictionary


def quitActivity(request):  # defining a function to quit an activity

    userid = request.COOKIES['userid']  # getting the userid from the request cookies
    activityid = request.GET.get('activityid')  # getting the activityid from the GET request

    user = User2.objects.get(id=userid)  # getting the user object with the userid
    activity = Activity.objects.get(id=activityid)  # getting the activity object with the activityid

    userActivity = UserActivity.objects.get(user=user,
                                            activity=activity)  # getting the UserActivity object with the user and activity objects
    userActivity.delete()  # deleting the UserActivity object

    return redirect('My Activity')  # redirecting to My Activity


# Define a function to handle uploading a photo for an activity
def uploadPhoto(request):

    # Check if the request method is POST
    if request.method == "POST":

        # Get the activity ID from the request's POST data
        userActivityId = request.POST.get("activity")

        userActitivity = UserActivity.objects.get(id=userActivityId)
        activityid = userActitivity.activity.id

        # Check if the activity ID is empty
        if activityid == '':
            # If it is, display an error message and redirect to the upload photo page
            messages.error(request, 'Activity ID cannot be empty.')
            return redirect('UploadPhoto')

        # Try to get the activity object using the activity ID
        try:
            activity = Activity.objects.get(id=activityid)
        except Activity.DoesNotExist:
            # If the activity does not exist, display an error message and redirect to the upload photo page
            messages.error(request, 'Activity does not exist.')
            return redirect('UploadPhoto')

        # Try to get the user ID from the request's cookies and get the user object using the user ID
        try:
            userid = request.COOKIES['userid']
            user = User2.objects.get(id=userid)
        except (KeyError, User2.DoesNotExist):
            # If the user is not logged in or does not exist, display an error message and redirect to the upload photo page
            messages.error(request, 'User not logged in.')
            return redirect('UploadPhoto')

        # Get the photo file from the request's POST data
        photo = request.FILES.get('photo')

        # Get the current date and time
        date = datetime.datetime.now()

        # Create a new UserPhotos object with the user, activity, photo, and date fields
        userPhoto = UserPhotos(user=user, activity=activity, photo=photo, date=date)

        # Save the new UserPhotos object
        userPhoto.save()

        # Display a success message and redirect to the activities page
        messages.success(request, 'Photo uploaded successfully.')
        return redirect('Activities')

    # If the request method is not POST, display the upload photo page with the upload photo form
    else:
        context = {}

        # Try to get the user ID from the request's cookies and get the user object using the user ID
        try:
            userid = request.COOKIES['userid']
            user = User2.objects.get(id=userid)

            # Create a new upload photo form object for the user
            context['form'] = UploadPhotoForm(user)
            context['userid'] = userid

            # Render the upload photo page with the context and return the response
            return render(request, 'uploadPhoto.html', context)
        except (KeyError, User2.DoesNotExist):
            # If the user is not logged in or does not exist, display an error message and redirect to the login page
            messages.error(request, 'User not logged in.')
            return redirect('Login')

# Define a function to render the user profile page
def userProfile(request):

    # Get the user ID from the cookie in the request

    try:
        # Retrieve user ID from cookies
        userid = request.COOKIES['userid']
    except Exception as e:
        return redirect('Login')

    # Get the profile user ID from the request
    profileUserId = request.GET.get('userid')

    # If there is no profile user ID, redirect to the home page
    if not profileUserId:
        return redirect('Home')

    else:
        # Get the user object using the user ID
        user = User2.objects.get(id=userid)
        # Get the profile user object using the profile user ID
        profileUser = User2.objects.get(id=profileUserId)
        # Get all the UserPhotos objects for the profile user
        profileUserPosts = UserPhotos.objects.filter(user=profileUser)

        # Check if the logged in user is following the profile user
        isFollowing = UserFollowings.objects.filter(follower=user, following=profileUser).exists()

        # Create a dictionary of data to pass to the template
        data = {'user': user, 'profileUser': profileUser, 'profileUserPosts': profileUserPosts, 'isFollowing': isFollowing }

        # Render the user profile page with the data
        return render(request, 'userProfile.html', data)

def follow(request):  # define a view function that handles the request to follow a user

    followerId = request.GET.get('followerId')  # get the ID of the follower from the request
    followingId = request.GET.get('followingId')  # get the ID of the user being followed from the request

    followerUser = User2.objects.get(id=followerId)  # get the follower user object from the database
    followingUser = User2.objects.get(id=followingId)  # get the user being followed object from the database

    userFollowing = UserFollowings(follower=followerUser, following=followingUser)  # create a new following relationship between the follower and the user being followed
    userFollowing.save()  # save the new following relationship to the database

    return redirect('/user-profile?userid=' + followingId)  # redirect the user to the profile page of the user being followed


# Defines a function to handle unfollowing a user
def unfollow(request):

    # Get the follower and following IDs from the GET request
    followerId = request.GET.get('followerId')
    followingId = request.GET.get('followingId')

    # Get the User2 objects for the follower and following
    followerUser = User2.objects.get(id=followerId)
    followingUser = User2.objects.get(id=followingId)

    # Get the UserFollowings object representing the follower following the followingUser
    userFollowing = UserFollowings.objects.get(follower=followerUser, following=followingUser)

    # Delete the userFollowing object from the database
    userFollowing.delete()

    # Redirect the user to the profile page of the user they unfollowed
    return redirect('/user-profile?userid=' + followingId)

def search(request):
    searchText = request.POST.get('search')

    return redirect('/user-list?search=' + searchText)