import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from app import settings


def get_recipe_image_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    
    return os.path.join('uploads/recipe', filename)    

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extras):
        if email == '':
            raise ValueError("Email address not provided")

        user = self.model(email=email, **extras)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extras):
        if email == '':
            raise ValueError("Email address not provided")
        user = self.model(email=email, **extras)
        user.set_password(password)
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.amount}"


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=get_recipe_image_file_path)
    
    def __str__(self):
        return self.title
