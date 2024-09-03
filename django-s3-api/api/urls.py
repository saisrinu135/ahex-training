from django.urls import path
from .views import ProfileView, home



urlpatterns = [
    path('profiles/', ProfileView.as_view(), name='profiles-list-create'),
    path('profiles/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
    path('home/', home, name='home')
]