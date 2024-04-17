from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as DjUser

from main.models import Ticket, Profile, Flight, User

admin.site.unregister(DjUser)
admin.site.register(User, UserAdmin)

admin.site.register(Ticket)
admin.site.register(Profile)
admin.site.register(Flight)

