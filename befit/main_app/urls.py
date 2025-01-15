from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('classes/', views.class_index, name='index'),
    path('accouts/signup/', views.signup, name="signup")

  
    
]