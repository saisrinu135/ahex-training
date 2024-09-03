from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager
# Create your models here.


class User(AbstractUser):
    """
User model that extends the AbstractUser class to use email as the unique identifier instead of a username.

This class defines a user with an email field that must be unique. The username field is set to None, and the email is used as the primary identifier for authentication.

Attributes:
    email (EmailField): The user's email address, which must be unique.

Methods:
    __str__(): Returns a string representation of the user, combining the first and last name.
"""

    username = None
    email = models.EmailField(unique=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.name