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

STATUS_TYPE = (
    ('PE', "Pending"),
    ('CA', "Canceled"),
    ('PA', "Paid"),
    ('NP', "Not Paid"),
    ('CO', "Completed"),
    ('RE', "Registered")
)

# Create your models here.

# Profile Model 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER, default = GENDER[0][0])
    weight = models.FloatField(default = 0.0)
    height = models.FloatField(default = 0.0)
    image = models.ImageField(upload_to='main_app/static/uploads/', default="/static/uploads/Profile-PNG-Photo_via79VZ.png")
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
    # trainer = models.ForeignKey(Trainer, on_delete = models.CASCADE)

    # direct the user to newly created page
    def get_absolute_url(self):
        return reverse('detail', kwargs={'gym_id': self.id})


    def __str__(self):
        return self.gym


class Trainer(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    image = models.ImageField(upload_to='main_app/static/uploads/', default="")
    specialties = models.CharField(max_length=100, default="No Specialty Specified")
    description = models.CharField(max_length=250)
    gym = models.ForeignKey(Gym, on_delete = models.CASCADE)

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=20)
    time = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    trainers = models.ManyToManyField(Trainer)
    # avalibility = models.BooleanField(default=True)
    price = models.FloatField(default=0.0)
    seats = models.IntegerField(default=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    


    def get_absolute_url(self):
        return reverse('session_detail', kwargs={'pk': self.id})
    
    
    def __str__(self):
        return self.name
        




class SubscriptionPackage(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user_type = models.CharField(max_length=2, choices=USER_TYPES,default=USER_TYPES[0][0])   

    def __str__(self):
        return f"{self.name} ({self.duration_days} days, {self.get_user_type_display()})"

    def get_absolute_url(self):
        return reverse('subscription_package_detail', kwargs={'pk': self.id})


class Subscription(models.Model):
    package = models.ForeignKey(SubscriptionPackage, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.CharField(max_length=20, default="Not Active")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.package.name} for {self.user.username}"

    def get_absolute_url(self):
        return reverse('subscription_detail', kwargs={'pk': self.id})  # Fix this to return a string

class Registration(models.Model):
        session = models.ForeignKey(Session,on_delete=models.CASCADE, default=1)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        date_registered = models.DateField()
        status = models.CharField(max_length=2, choices=STATUS_TYPE, default=STATUS_TYPE[0][0])
        comment = models.CharField(default="", max_length=250)
    
        def __str__(self):
            return self.name


