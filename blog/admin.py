from re import T
from django.contrib import admin
from .models import Course, Category, Teacher, Headline, Comment, Like, Video, Buy, CourseChat, Room, Basket,Token,Message

# Register your models here.

@admin.register(Message)
class Tokendmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Token)
class Tokendmin(admin.ModelAdmin):
    list_display = ('user', 'token')
    ordering = ('user', 'token')
    search_fields = ('user', 'token')

@admin.register(Basket)
class Basketdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    ordering = ('user', 'course')
    search_fields = ('user', 'course')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'admin')
    search_fields = ('room_name', 'admin')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment')
    search_fields = ('user', 'comment')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'upload_date', 'category')
    ordering = ('name', 'upload_date', 'category')
    search_fields = ('name', 'upload_date', 'category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'parent')
    ordering = ('name', 'course', 'parent')
    search_fields = ('name', 'course', 'parent')

@admin.register(Headline)
class HeadlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    ordering = ('name', 'course')
    search_fields = ('name', 'course')

@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    ordering = ('user', 'course')
    search_fields = ('user', 'course')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('course', 'head_line', 'demo')
    ordering = ('course',)
    search_fields = ('course', 'head_line', 'demo')

@admin.register(CourseChat)
class CourseChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'course')
    ordering = ('date',)
    search_fields = ('user', 'date',)