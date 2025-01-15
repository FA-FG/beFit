from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gyms/', views.class_index, name='index'),
    path('accouts/signup/', views.signup, name="signup"),
    path('gyms/<int:gym_id>/', views.gyms_detail, name="detail"),
    path('gyms/create/', views.GymCreate.as_view(), name='gyms_create'),
    # CBV's
    path('gyms/<int:pk>/update', views.GymUpdate.as_view(), name='gyms_update'),
    path('gyms/<int:pk>/delete', views.GymDelete.as_view(), name='gyms_delete'),

  
    
]