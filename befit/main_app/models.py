from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


GENDER = (
    ('M', 'Male'),
    ('F', 'Female')
)

USER_TYPES = (
    ('NU', 'Normal User'),
    ('GO', 'GYM Owner')
)

# Create your models here.

# Profile Model 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER, default = GENDER[0][0])
    weight = models.FloatField(default = 0.0)
    height = models.FloatField(default = 0.0)
    image = models.ImageField(upload_to='main_app/static/uploads/', default="")

    type = models.CharField(max_length=2, choices=USER_TYPES, default = USER_TYPES[0][0])

    isSubscribed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_id': self.id})


    def __str__(self):
        return self.user.username

  



# Gyn Model

class Gym(models.Model):
    gym = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phoneNumber = models.CharField()
    description = models.CharField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # direct the user to newly created page
    def get_absolute_url(self):
        return reverse('detail', kwargs={'gym_id': self.id})


    def __str__(self):
        return self.gym


class Session(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=20)
    time = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    trainer = models.CharField(max_length=50)
    avalibility = models.BooleanField(default=True)
    price = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def get_absolute_url(self):
        return reverse('session_detail', kwargs={'pk': self.id})
    
    
    def __str__(self):
        return self.name
        
