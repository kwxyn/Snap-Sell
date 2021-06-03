from django.db import models
from django.contrib.auth.models import User
# accounts app

# Create your models here.

class UserProfile(models.Model):
    avatar = models.ImageField(default='accounts/user_default.gif', upload_to='accounts/') # Picture of user
    user = models.OneToOneField(User, on_delete=models.CASCADE) # reference to User Table


    def __str__(self):
        return self.user.username