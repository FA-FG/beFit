from django.urls import path
from . import views
from .views import profile



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('classes/', views.class_index, name='index'),
    path('accouts/signup/', views.signup, name="signup"),
    #profile path
    path('profile/', profile, name='profile'),
    
    ## add profile info
    path('profile/create/', views.ProfileCreate.as_view(), name='profile_create')


    
]