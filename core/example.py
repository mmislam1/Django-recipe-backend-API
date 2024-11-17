from django.db import models

# Many-to-many
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    publish_date = models.DateField()
    authors = models.ManyToManyField(Author, through='BookAuthor')
    
class BookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contribution_date = models.DateField()
    role = models.CharField(max_length=50)
    
# Self-referential many-to-many
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    friend_list = models.ManyToManyField('self', symmetrical=False, related_name='friend')
    
# Complex structure
class Department(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subdepartments')

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')
