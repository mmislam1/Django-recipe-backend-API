from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extras):
        user=self.model(email,**extras)
        user.set_password(password)

        user.save()

        return user
    

    
