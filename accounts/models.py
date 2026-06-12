from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser): # Add this class for custom user model
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)

    profile_picture = models.ImageField(upload_to='user_profile', blank=True, null=True)
    