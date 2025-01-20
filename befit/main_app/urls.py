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



    path('subscriptions/packages/', views.subscription_package_list, name='subscription_package_list'),
    path('subscriptions/subscribe/<int:package_id>/', views.subscribe_to_package, name='subscribe_to_package'),
    path('subscriptions/my/', views.view_my_subscriptions, name='view_my_subscriptions'),



    path('session/', views.SessionList.as_view(), name='session_index'),
    path('session/<int:pk>/', views.SessionDetail.as_view(), name='session_detail'),
    path('session/create/', views.SessionCreate.as_view(), name='session_create'),
    path('session/<int:pk>/update/', views.SessionUpdate.as_view(), name='session_update'),
    path('session/<int:pk>/delete/', views.SessionDelete.as_view(), name='session_delete'),



    
]