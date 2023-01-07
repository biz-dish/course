import random
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .forms import CourseForm, RegisterUserForm, HeadlineForm, CommentForm, VideoForm, CourseChatForm, RoomForm, MessageForm
from .models import Course, Category, Headline, Teacher, Comment, Like, Video, Buy, CourseChat, Room, Message, Basket, Token
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view
from .serializers import *
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

class MyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try :
            room = Room.objects.get(id=view.kwargs['room_id'])
            return bool(request.user in room.members.all())
        except Room.DoesNotExist:
            return False
        
class MessageList(APIView):
    permission_classes = ([MyPermission])
    def get(self, request, room_id):
        message = Message.objects.filter(room=room_id)
        serializer = MessageSerializer(message, many=True)
        #if request.user in room.members.all():     
        #    return Response(serializer.data)
        #else:
        #    return Response("You Are Not Member Of This Room") 

        return Response(serializer.data)

def cache_cl(request):
    cache.clear()
    return redirect('home')

def message_list(request, room_id):
    id = room_id
    room = Room.objects.get(pk=id)
    #response = requests.get('http://127.0.0.1:8000/api_message/').json()

    return render(
        request,
        'message_list.html',
        {
            #'response':response
            "id":id,
            "room":room
        }
    )  

def post_message(request, room_id):
    id = room_id
    room = Room.objects.get(pk=id)
    return render(
        request,
        'post_message.html',
        {
            "id":id,
            "room":room
        }
    )

@api_view(['GET'])
def get_message(request):
    message = Message.objects.all()
    serializer_context = {
            'request': request,
        }
    serializer = MessageSerializer(message, context=serializer_context, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_message(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def get_data(request):
    course = Course.objects.all()
    serializer_context = {
            'request': request,
        }
    serializer = CourseSerializer(course, context=serializer_context, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_s_data(request, course_id):
    course = Course.objects.get(pk=course_id)
    serializer_context = {
            'request': request,
        }
    serializer = CourseSerializer(course, context=serializer_context)
    return Response(serializer.data)

@api_view(['POST'])
def add_data(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def get_data_cat(request):
    cat = Category.objects.all()
    serializer_context = {
            'request': request,
        }
    serializer = CategorySerializer(cat, context=serializer_context, many=True)
    return Response(serializer.data)

@login_required
def chat(request, room_id):
    room = Room.objects.get(pk=room_id)
    chat = Message.objects.filter(room=room_id)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():

            form = form.save(commit=False)
            form.user = request.user
            form.room = room
            form.save()
            return redirect('chat', room_id)

    else:
        form = MessageForm

    return render(
        request,
        'chat.html',
        {
            'form': form,
            'chat': chat,
            'room': room
        }
    )


@login_required
def rooms_list(request):
    rooms = Room.objects.filter(members=request.user)

    return render(
        request,
        'rooms_list.html',
        {"room": rooms, }
    )


@login_required
def room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            t_form = form.save(commit=False)
            t_form.admin = request.user
            t_form.save()
            messages.success(
                request, "!!! Your Room Submitted Successfully !!!")
            return redirect('home')

        else:
            messages.success(request, "!!! try again !!!")

    else:
        form = RoomForm

    return render(
        request,
        'add_room.html',
        {'form': form}
    )


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        course = Course.objects.filter(name__contains=searched)
        if searched:
            return render(
                request,
                'search.html',
                {"searched": searched, "course": course},
            )
        else:
            return render(
                request,
                'search.html',
                {"searched": searched}
            )
    else:
        return render(
            request,
            'search.html',
            {},
        )


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')
            return redirect('home')
        else:
            messages.success(request, 'There Is A Problem, Pleas Try Again!')
            return redirect('login')
    else:
        pass

    return render(
        request,
        'login.html',
        {
        }
    )


@login_required
def chang_password(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        new_password = request.POST['new_password']
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Changing Password Successful!')
        return redirect('home')

    return render(
        request,
        'chang_password.html',
        {
        }
    )


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'register Successful!')
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout Successful!')
    return redirect('home')

def home(request):
    top_course = Course.objects.order_by('-concession')[0]
    random_course = Course.objects.order_by('?')[0]
    c = {
        "random_course": random_course,
        "top_course": top_course,  
    }
    if request.user.is_authenticated:
        b_course = Course.objects.filter(buyer=request.user)
        cat = b_course.values_list('category', flat=True).distinct()
        try:
            random_cat = random.randint(0, len(cat))
            s_course = Course.objects.filter(category=cat[random_cat])
            c = {
                "random_course": random_course,
                "top_course": top_course,
                "bcourse": b_course,
                "s_course": s_course,   
            }
        
        except IndexError:
            c = {
                "random_cat": random_cat,
                "random_course": random_course,
                "top_course": top_course,
                "bcourse": b_course,
            }
                       

    return render(
        request,
        'home.html',
        c
    )



def my_dec(func):
    def my_warp(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                request.user.teacher
            except Teacher.DoesNotExist:
                messages.success(
                    request, "!!! only teachers can add course !!!")
                return redirect('home')
            else:
                return func(request, *args, **kwargs)

        else:
            messages.success(request, "!!! PLS login first !!!")
            return redirect('login')

    return my_warp


@my_dec
def add_course(request):
    # if request.user.teacher: #if request.user.is_authenticated=>(@login_required) request.user.teacher:
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            t_form = form.save(commit=False)
            t_form.teacher = request.user
            t_form.save()
            messages.success(
                request, "!!! Your Course Submitted Successfully !!!")
            return redirect('home')

        else:
            messages.success(request, "!!! try again !!!")

    else:
        form = CourseForm

    return render(
        request,
        'add_course.html',
        {'form': form}
    )


def course_list(request):
    courses = Course.objects.all()
    category = Category.objects.all()
    p = Paginator(courses, 3)
    page = request.GET.get('page')
    course_page = p.get_page(page)

    return render(
        request,
        'course_list.html',
        {"courses": course_page, "category": category}
    )
def course_list_byV(request):
    courses = Course.objects.order_by('-views')
    category = Category.objects.all()
    p = Paginator(courses, 3)
    page = request.GET.get('page')
    course_page = p.get_page(page)

    return render(
        request,
        'course_list.html',
        {"courses": course_page, "category": category}
    )
def course_list_byC(request):
    courses = Course.objects.order_by('-concession')
    category = Category.objects.all()
    p = Paginator(courses, 3)
    page = request.GET.get('page')
    course_page = p.get_page(page)

    return render(
        request,
        'course_list.html',
        {"courses": course_page, "category": category}
    )

def course_category(request, category_id):
    courses = Course.objects.filter(category=category_id)

    p = Paginator(courses, 2)
    page = request.GET.get('page')
    course_page = p.get_page(page)

    return render(
        request,
        'course_category.html',
        {"courses": course_page, }
    )


def video(request, headline_id):
    headline = Headline.objects.get(pk=headline_id)
    course = Course.objects.get(name=headline.course.name)
    video = Video.objects.filter(head_line=headline_id)

    return render(
        request,
        'videos.html',
        {
            "headline": headline,
            "video": video,
            "course": course,
        }
    )


def course(request, course_id):

    course = Course.objects.get(pk=course_id)



    #if cache.get('s_course'):
        #s_course = cache.get('s_course')
        #print('________________from CH__________________')
    #else:
    s_course = Course.objects.filter(category=course.category)
        #cache.set('s_course', s_course)
        #print('________________from DB__________________')

    if course:
        if course.viewers == None:
            course.viewers = ""
            course.save()
        if request.user.is_authenticated and request.user.username not in course.viewers:
            course.views = course.views + 1
            course.viewers += request.user.username
            course.viewers += ", "
            course.save()

    headline = Headline.objects.filter(course=course_id)

    comment = Comment.objects.filter(course=course_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay = form.save(commit=False)
                    replay.parent = parent_obj
                    replay.course = course
                    replay.sender = request.user
                    replay.save()
                    messages.success(
                        request, "!!! Your Replay Comment Submitted Successfully !!!")
                    return redirect('course', course_id)
            t_form = form.save(commit=False)
            t_form.course = course
            t_form.sender = request.user
            t_form.save()
            messages.success(
                request, "!!! Your Comment Submitted Successfully !!!")
            return redirect('course', course_id)

        else:
            messages.success(request, "!!! try again !!!")

    else:
        form = CommentForm

    return render(
        request,
        'course.html',
        {
            "headline": headline,
            "course": course,
            "comment": comment,
            "form": form,
            "s_course": s_course,
        }
    )

def update(request, course_id):
    course = Course.objects.get(pk=course_id)
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            key = make_template_fragment_key('s_course', [course.id])
            cache.delete(key)
            messages.success(request, "!!! Course Updated !!!", extra_tags="success")
            return redirect('course', course_id)
    return render(
        request,
        'update.html',
        {
            "course": course,
            "form": form,
        }
    )            


@login_required
def add_headline(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.user == course.teacher:
        if request.method == "POST":
            form = HeadlineForm(request.POST)
            if form.is_valid():
                t_form = form.save(commit=False)
                t_form.course = course
                t_form.save()
                messages.success(
                    request, "!!! Your Headline Submitted Successfully !!!")
                return redirect('home')

            else:
                messages.success(request, "!!! try again !!!")

        else:
            form = HeadlineForm

        return render(
            request,
            'add_headline.html',
            {'form': form}
        )
    else:
        messages.success(request, "!!! Permission Denied !!!")
        return redirect('home')


@login_required
def add_video(request, headline_id):
    headline = Headline.objects.get(pk=headline_id)
    if request.user == headline.course.teacher:
        if request.method == "POST":
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                t_form = form.save(commit=False)
                t_form.course = headline.course
                t_form.head_line = headline
                t_form.save()
                messages.success(
                    request, "!!! Your Headline Submitted Successfully !!!")
                return redirect('home')

            else:
                messages.success(request, "!!! try again !!!")

        else:
            form = VideoForm

        return render(
            request,
            'add_video.html',
            {'form': form}
        )
    else:
        messages.success(request, "!!! Permission Denied !!!")
        return redirect('home')


@login_required
def video_formset(request, headline_id):
    headline = Headline.objects.get(pk=headline_id)
    if request.user == headline.course.teacher:
        VideoFormSet = formset_factory(VideoForm, extra=0, max_num=10)
        if request.method == "POST":
            formset = VideoFormSet(request.POST, request.FILES or None)
            if formset.is_valid():
                for form in formset:
                    form = form.save(commit=False)
                    form.course = headline.course
                    form.head_line = headline
                    form.save()

                messages.success(
                    request, "!!! Your Headline Submitted Successfully !!!")
                return redirect('home')

            else:
                messages.success(request, "!!! try again !!!")
        else:
            formset = VideoFormSet

    else:
        messages.success(request, "!!! Permission Denied !!!")
        return redirect('home')

    return render(
        request,
        'video_formset.html',
        {'formset': formset}
    )


@login_required
def like(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.method == "POST":

        newLike = Like(user=request.user, comment=comment)

        comment.like += 1
        comment.likers.add(request.user)
        comment.save()
        newLike.save()
        messages.success(request, "!!! Liked !!!")

    id = comment.course.id
    return redirect('course', id)


@login_required
def dislike(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.method == "POST":

        dislike = Like(user=request.user, comment=comment)

        comment.like -= 1
        comment.likers.remove(request.user)
        comment.save()
        dislike.save()
        messages.success(request, "!!! Disliked !!!")

    id = comment.course.id
    return redirect('course', id)


@login_required
def basket(request, course_id):
    course = Course.objects.get(pk=course_id)

    if request.method == "POST":

        basket = Basket(user=request.user, course=course)
        if Basket.objects.filter(user=request.user, course=course).exists():
            messages.success(
                request, "!!!  this cours allredy is in your basket  !!!")

        else:
            basket.save()
            messages.success(
                request, "!!!  cours save in basket successfully  !!!")

    return redirect('basket-list')


@login_required
def basket_list(request):
    baskets = Basket.objects.filter(user=request.user)

    return render(
        request,
        'basket_list.html',
        {
            'basket': baskets
        }
    )

def delete_basket(request, basket_id):
    delete = Basket.objects.get(pk=basket_id)
    if request.method == 'POST':
        delete.delete()
        messages.success(request, "!!! Basket Deleted !!!")
    return redirect('basket-list')


def set_session(request, course_id):
    course = Course.objects.get(pk=course_id)
    request.session[course_id] = course.pk
    return HttpResponse("session is set")

def get_session(request, course_id):
    id = request.session[course_id]
    course = Course.objects.get(pk=id)
    return HttpResponse(course)

def all_sessions(request):
    for key in request.session.items():
        print(key)
    courses = Course.objects.all()
    list_id = courses.values_list(flat=True)
    sessions = []
    for key in list_id:
        if request.session.get(str(key)):
            sessions.append(key)
    course = Course.objects.filter(pk__in=sessions)
    return HttpResponse(course)



@login_required
def buy(request, course_id):
    course = Course.objects.get(pk=course_id)

    if request.method == "POST":

        buy_course = Buy(user=request.user, course=course)
        course.buyer.add(buy_course.user)
        if Token.objects.filter(user=request.user).exists():
            token = Token.objects.get(user=request.user)
            token.token = token.token + 1
            token.save()
        else:
            token = Token(user=request.user, token=1)
            token.save()
        buy_course.save()
        messages.success(
            request, "!!!  The purchase was made successfully  !!!")

    return redirect('course', course_id)


@login_required
def tbuy(request, course_id):
    token = Token.objects.get(user=request.user)
    course = Course.objects.get(pk=course_id)

    if request.method == "POST":
        
        if course.tbuy == True:
            if token.token > 99:
                buy_course = Buy(user=request.user, course=course)
                course.buyer.add(buy_course.user)
                token = Token.objects.get(user=request.user)
                token.token = token.token - 100
                token.save()

                buy_course.save()
                messages.success(request, "!!!  The purchase was made successfully  !!!")
            else:
                messages.success(request, "!!!  You Do Not Have 100 or mor than 100 token  !!!")
        else:
            messages.success(request, "!!!  You Can Not Buy This Course With Token  !!!")

    return redirect('course', course_id)


@login_required
def course_chat(request, course_id):
    course = Course.objects.get(pk=course_id)
    chat = CourseChat.objects.filter(course=course_id)
    if request.method == "POST":
        form = CourseChatForm(request.POST)
        if form.is_valid():

            form = form.save(commit=False)
            form.user = request.user
            form.course = course
            form.save()
            return redirect('course_chat', course_id)

    else:
        form = CourseChatForm

    return render(
        request,
        'base_chat.html',
        {
            'form': form,
            'chat': chat,
            'course': course
        }
    )



'''
HTML
<form method="POST" action="{% url 'home' %}">
    {% csrf_token %}
    <h3>Your Email: <br><input name="user_email" type="email"></h3><br>
    <h3>Messages: <br><input type="text" name="message"></h3><br>
    <input type="submit" value="Submit" class="btn btn-dark"><br><br>
</form><hr>
DJANGO
if request.method == "POST":
    user_email = request.POST['user_email']
    message = request.POST['message']
    messages.success(request, 'Send Email Successful!')

    from django.core.mail import send_mail
    send_mail(
        'Subject here',
        message,
        user_email,
        ['nagisa.tate@gmail.com'],
        fail_silently=False,
    )
    return render(
        request,
        'home.html',
        {"user_email": user_email}
    )
'''