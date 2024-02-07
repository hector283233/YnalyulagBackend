from django.urls import path

from . import views

urlpatterns = [
    path('locations-list/', views.LocationsList.as_view(), name="locations-list"),
    path('transport-create/', views.TransportCreate.as_view(), name='transport-create'),
    path('transport-update/<int:pk>/', views.TransportUpdate.as_view(),
         name='transport-update'),
    path('transport-delete/<int:pk>/', views.TransportDelete.as_view(),
         name='transport-delete'),
    path('trip-create/', views.TripCreate.as_view(), name='trip-create'),
    path('trip-update/<int:pk>/', views.TripUpdate.as_view(), name='trip-update'),
    path('trip-delete/<int:pk>/', views.TripDelete.as_view(), name='trip-delete'),
    path('trip-list/', views.TripFilter.as_view(), name='trip-list'),
    path('trip-detail/<int:pk>/', views.TripDetail.as_view(), name="trip-detail"),
    path('comment-create/', views.CommentCreate.as_view(),
         name="comment-create"),
    path('comment-update/<int:pk>/', views.CommentUpdate.as_view(),
         name='comment-update'),
    path('comment-delete/<int:pk>/', views.CommentDelete.as_view(),
         name="comment-delete"),
    path('trip-active-toggle/<int:pk>/<int:pk>/', views.TripActiveToggle.as_view(),
        name="trip-active-toggle"),
]