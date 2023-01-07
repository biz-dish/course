from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Teacher(User):
    name = models.CharField('Name', max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)
    parents = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, default=None, blank=True, related_name='children',
        )

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    upload_date = models.DateField('Upload Date', auto_now_add=True)
    file = models.FileField(upload_to = 'uploaded', null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, default=None, blank=True, related_name='category')
    views = models.IntegerField(default=0)
    concession = models.IntegerField(default=0)
    viewers = models.TextField(default="", null=True, blank=True)
    price = models.CharField(default="$0", max_length=100)
    buyer = models.ManyToManyField(User, related_name='buyer', default=None, blank=True)
    tbuy = models.BooleanField(null=True)

    def __str__(self):
        return self.name


class Buy(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)



class Headline(models.Model):
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None, blank=True)

    def __str__(self):
        return self.name
    

class Video(models.Model):
    head_line = models.ForeignKey(Headline, on_delete=models.CASCADE, null=True, default=None, blank=True)
    file = models.FileField(upload_to = 'uploaded', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None, blank=True)
    demo = models.BooleanField()

class Comment(models.Model):
    name = models.CharField('Name', max_length=100, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None, blank=True)
    pov = models.TextField('Point of view', null=True)
    parent = models.ForeignKey('self', null=True, default=None, on_delete=models.CASCADE, blank=True, related_name='replies')
    like = models.IntegerField(default=0)
    likers = models.ManyToManyField(User, related_name='likers', default=None, blank=True)

    def __str__(self):
        return self.name

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, default=None, blank=True, related_name='comments')


class CourseChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    date = models.DateField(auto_now_add=True)
    message = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None, blank=True)


class Room(models.Model):
    admin = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name = 'admin')
    members = models.ManyToManyField(User, related_name = 'members')
    room_name = models.CharField(max_length = 128, unique=True)

class Message(models.Model):
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL, related_name = 'room')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    date = models.DateField(auto_now_add=True)
    message = models.TextField()
    
class Basket(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    token = models.IntegerField(default=0)

'''
language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='python')
course_type = models.CharField(max_length=15, choices=COURSE_CHOICES, default='Programming')
    
LANGUAGE_CHOICES = [
    ('Python', 'PYTHON'),
    ('c++', 'C++'),
    ('c', 'C'),
    ('java', 'JAVA'),
]
COURSE_CHOICES = [
    ('security','SECUTITY'),
    ('network','NETWORK'),
    ('programming','PROGRAMMIN'),
]
'''

