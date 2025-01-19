from django.urls import path
from . import views
from .views import profile, Trainer



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



    path('session/', views.SessionList.as_view(), name='session_index'),
    path('session/<int:pk>/', views.SessionDetail.as_view(), name='session_detail'),
    path('session/create/', views.SessionCreate.as_view(), name='session_create'),
    path('session/<int:pk>/update/', views.SessionUpdate.as_view(), name='session_update'),
    path('session/<int:pk>/delete/', views.SessionDelete.as_view(), name='session_delete'),

    # trainer
    path('trainer/<int:pk>/', views.TrainerDetail.as_view(), name="trainer_detail"),
    path('trainer/create/', views.TrainerCreate.as_view(), name="trainer_create"),
    path('trainer/<int:pk>/update/', views.TrainerUpdate.as_view(), name="trainer_update"),
    path('trainer/<int:pk>/delete/', views.TrainerDelete.as_view(), name="trainer_delete"),

    
]