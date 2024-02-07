from django.urls import path, include

urlpatterns = [
    # Ендпоинт для авторизации и пользователей
    path('auth/', include('api.auth.urls')),
    path('transport/', include('api.transport.urls')),
]