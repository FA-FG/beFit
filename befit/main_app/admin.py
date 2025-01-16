from django.contrib import admin
from .models import Gym, Session, Registration

# Register your models here.
admin.site.register(Gym)
admin.site.register(Session)
admin.site.register(Registration)