from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('cache', views.cache_cl, name='cache'),
    path('search/', views.search, name='search'),
    path('buy/<course_id>', views.buy, name='buy'),
    path('login/', views.login_user, name="login"),
    path('tbuy/<course_id>', views.tbuy, name='tbuy'),
    path('logout/', views.user_logout, name="logout"),
    path('register/', views.register, name="register"),
    path('basket/<course_id>', views.basket, name='basket'),
    path('course/<course_id>', views.course, name='course'),
    path('upcourse/<course_id>', views.update, name='upcourse'),
    path('add_course/', views.add_course, name='add_course'),
    path('videos/<headline_id>', views.video, name='videos'),
    path('basket_list', views.basket_list, name='basket-list'),
    path('delete_basket/<basket_id>', views.delete_basket, name='delete'),
    path('add_video/<headline_id>', views.add_video, name='add_video'),
    path('chang_password/', views.chang_password, name='chang_password'),
    path('add_headline/<course_id>', views.add_headline, name='add_headline'),
    path('course_category/<category_id>', views.course_category, name='category'),
    path('video_formset/<headline_id>', views.video_formset, name='video_formset'),
    # like
    path('like/<comment_id>', views.like, name='like'),
    path('dislike/<comment_id>', views.dislike, name='dislike'),
    # chat
    path('add_room/', views.room, name='add_room'),
    path('chat/<room_id>', views.chat, name='chat'),
    path('your_rooms', views.rooms_list, name='rooms_list'),
    path('course_chat/<course_id>', views.course_chat, name='course_chat'),
    # chat API
    path('message_list2/<room_id>', views.MessageList.as_view()),
    path('api_message/', views.get_message),
    path('add_message/', views.add_message),
    path('message_list/<room_id>', views.message_list, name='message_list'),
    path('post_message/<room_id>', views.post_message, name='post_message'),
    # list
    path('course_list/', views.course_list, name='course_list'),
    path('course_list_byC/', views.course_list_byC, name='course_list_byC'),
    path('course_list_byV/', views.course_list_byV, name='course_list_byV'),
    # API
    path('api/', views.get_data),
    path('api/<course_id>', views.get_s_data),   
    path('add_api/', views.add_data),
    path('cat_api/', views.get_data_cat),
    path('api-auth/', include('rest_framework.urls')),
    # session
    path('set/<course_id>', views.set_session, name='set'),
    path('get/<course_id>', views.get_session, name='get'),
    path('all/', views.all_sessions, name='all_sessions'),




]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
