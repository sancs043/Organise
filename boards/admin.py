from django.contrib import admin

# Register your models here.

from .models import Activity
from .models import User2
from .models import UserActivity
from .models import UserPhotos
from .models import UserFollowings

admin.site.register(Activity)
admin.site.register(User2)
admin.site.register(UserActivity)
admin.site.register(UserPhotos)
admin.site.register(UserFollowings)
