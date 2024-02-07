from django.urls import path

from . import views_old

# Ендпоинты для авторизации
urlpatterns = [
    path('login/', views_old.LoginUser.as_view(), name='login'),
    path('register-mobile/', views_old.registerMobile, name='register-mobile'),
    path('sms-list/', views_old.smsList, name='sms-list'),
]