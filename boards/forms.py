# dwitter/forms.py

from django import forms # Import the forms module from the django library
from .models import Activity, UserPhotos, UserActivity # Import the Activity, UserPhotos, and UserActivity models from the current directory's models.py file

class LoginForm(forms.Form): # Create a form class named LoginForm that inherits from the Form class
    email = forms.EmailField(required=True) # Create a field named email, with a label 'Email' and required to be filled
    password = forms.CharField(widget=forms.PasswordInput()) # Create a password field named password and provide a widget to mask the input

    class Meta: # Define the class for the Meta configuration
        exclude = ("user", ) # Exclude the user field

class RegisterForm(forms.Form): # Create a form class named RegisterForm that inherits from the Form class
    email = forms.EmailField(required=True) # Create a field named email, with a label 'Email' and required to be filled
    password = forms.CharField(required=True, widget=forms.PasswordInput()) # Create a password field named password and provide a widget to mask the input
    name = forms.CharField(required=True, max_length=150) # Create a field named name with a maximum length of 150 characters
    surname = forms.CharField(required=True, max_length=150) # Create a field named surname with a maximum length of 150 characters

    class Meta: # Define the class for the Meta configuration
        exclude = ("user", ) # Exclude the user field

class CreateActivityForm(forms.Form): # Create a form class named CreateActivityForm that inherits from the Form class
    name = forms.CharField(max_length=50) # Create a field named name with a maximum length of 50 characters
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"rows":"5"})) # Create a field named description with a maximum length of 500 characters and use Textarea widget to allow multiline text
    date = forms.DateField(widget=forms.SelectDateWidget()) # Create a field named date that will use SelectDateWidget as its input widget
    maxPeople = forms.IntegerField() # Create a field named maxPeople that is an integer
    location = forms.CharField(max_length=50) # Create a field named location with a maximum length of 50 characters

class EditActivityForm(forms.ModelForm): # Create a form class named EditActivityForm that inherits from the ModelForm class
    name = forms.CharField(max_length=50) # Create a field named name with a maximum length of 50 characters
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"rows":"5"})) # Create a field named description with a maximum length of 500 characters and use Textarea widget to allow multiline text
    date = forms.DateField(widget=forms.SelectDateWidget()) # Create a field named date that will use SelectDateWidget as its input widget
    maxPeople = forms.IntegerField() # Create a field named maxPeople that is an integer
    location = forms.CharField(max_length=50) # Create a field named location with a maximum length of 50 characters

    class Meta: # Define the class for the Meta configuration
        model = Activity # Use the Activity model
        exclude = ("creator", ) # Exclude the creator field

class UploadPhotoForm(forms.ModelForm): # Defines a new form called UploadPhotoForm that inherits from forms.ModelForm.

    def __init__(self, user, *args, **kwargs): # Initializes the UploadPhotoForm with a user parameter and any additional arguments passed through *args and **kwargs.
        self.user = user # Assigns the user parameter to the form's user attribute.

        super(UploadPhotoForm, self).__init__(*args, **kwargs) # Calls the __init__ method of the parent class, passing any additional arguments through.

        userJoinedActivities = UserActivity.objects.filter(user=self.user) # Retrieves all activities that the user has joined.

        self.fields['activity'].queryset = userJoinedActivities # Assigns the user's joined activities queryset to the activity field of the form.

    photo = forms.ImageField() # Defines a photo field for the form, which is an image field that the user will use to upload a photo.

    class Meta:
        model = UserPhotos # Defines the model that this form is associated with as UserPhotos.
        exclude = ("user", "date") # Specifies the fields that should be excluded from the form, namely "user" and "date".




