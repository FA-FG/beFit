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
    path('profile/create/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),

    #GYM
    path('gyms/', views.class_index, name='index'),
    path('accouts/signup/', views.signup, name="signup"),
    path('gyms/<int:gym_id>/', views.gyms_detail, name="detail"),
    path('gyms/create/', views.GymCreate.as_view(), name='gyms_create'),
    # CBV's
    path('gyms/<int:pk>/update', views.GymUpdate.as_view(), name='gyms_update'),
    path('gyms/<int:pk>/delete', views.GymDelete.as_view(), name='gyms_delete'),
    
]