from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register-mobile/', views.registerMobile, name='register-mobile'),
    path('sms-list/', views.smsList, name='sms-list'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('driver-list/', views.DriversList.as_view(), name='driver-list'),
    path('driver-detail/<int:pk>/', views.DriverDetail.as_view(), name="driver-detail"),
    path('user-detail/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]