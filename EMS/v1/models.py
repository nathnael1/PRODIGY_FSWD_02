from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username=username)
    
class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    objects = UserManager()
