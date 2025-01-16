from django.contrib import admin
from .models import Gym, Session, Profile

# Register your models here.
admin.site.register(Gym)
admin.site.register(Session)
admin.site.register(Profile)
