from django.urls import  path
from .views import UserView, LoginView, StudentView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# registering viewsets routes to router
router.register('users', UserView, basename='users')
router.register('students', StudentView, basename='students')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += router.urls
