from django import forms
from .models import Course, Headline, Comment, Video, CourseChat, Room, Message
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = (
            'message',

        )
        labels = {
            'message': 'Your Message ',

        }

        widgets = {
            
            'message': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Hi guys ...'}),

        }

class CourseChatForm(ModelForm):
    class Meta:
        model = CourseChat
        fields = (
            'message',

        )
        labels = {
            'message': 'Your Message ',

        }

        widgets = {
            
            'message': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Hi guys ...'}),

        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = (
            'name',
            #'sender',
            #'course',
            'pov',
        )
        labels = {
            'name': 'Your Name ',
            'pov': 'Point of view ',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Peter'}),           

            'pov': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Point of view'}),

        }


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = (
            'name',
            'file',
            'description',
            'category',
            #'teacher',
            'price',
            'tbuy',
        )

        labels = {
            'name': 'Course Name ',
            'file': 'File ',
            'description': 'Description ',
            'category': 'Course category',
            #'teacher': 'Teacher',
            'price': 'Price',
            'tbuy': 'Token Buy',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Input Your Course Name'}),           
            
            'file': forms.FileInput(
                attrs={'class': 'form-select', 'placeholder': 'Input Course File'}),

            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Input Course Description'}),
        
            'category': forms.Select(
                attrs={'class': 'form-select', 'placeholder': 'Input Course category'}),

            #'teacher': forms.Select(
                #attrs={'class': 'form-select', 'placeholder': 'Input Course teacher'}),

            'price': forms.TextInput(
                attrs={'class': 'form-select', 'placeholder': '$'}),

            'tbuy': forms.CheckboxInput(
                attrs={'placeholder': 'Buy Your Course With Token'}),
            }


class HeadlineForm(ModelForm):
    class Meta:
        model = Headline
        fields = (
            'name',
            'description',
            #'course',
        )

        labels = {
            'name': 'Headline Name ',
            'description': 'Description ',
            #'course': 'Course ',

        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Input Your Course Name'}),           

            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Input Course Description'}),
        
            #'course': forms.Select(
                #attrs={'class': 'form-select', 'placeholder': 'Input Course '}),

        }



class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = (
            'file',
            'demo',
        )

        labels = {
            'file': 'File ',
            'demo': 'Demo',
        }

        widgets = {
            'file': forms.FileInput(
                attrs={'class': 'form-select', 'placeholder': 'Input Course File'}),

            'demo': forms.CheckboxInput(
                attrs={}),
        }


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = (
            'members',
            'room_name',
        )

        labels = {
            'members': 'Members',
            'room_name': 'Room Name',
        }

        widgets = {
            'members': forms.SelectMultiple(
                attrs={'class': 'form-select', 'placeholder': 'Members'}),

            'room_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Input Rooms Name'}), 
        }