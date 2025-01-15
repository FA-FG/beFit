from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


GENDER = (
    ('F', 'Female'),
    ('M', 'Male')
)


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField()
    gender = models.CharField(max_length=6)
    weight = models.FloatField(default = 0.0)
    height = models.FloatField(default = 0.0)
    image = models.ImageField(upload_to='main_app/static/uploads/', default="")
    isSubscribed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('index', kwargs={'profile_id':self.id})

    def __str__(self):
        return self.user.username

