from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Gym(models.Model):
    gym = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phoneNumber = models.CharField()
    description = models.CharField()
  

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
    gym = models.ForeignKey(Gym,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def get_absolute_url(self):
        return reverse('session_detail', kwargs={'pk': self.id})
    
    
    def __str__(self):
        return self.name
        



    