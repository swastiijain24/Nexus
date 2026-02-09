from django.urls import path
from rtchat import views

urlpatterns =[
    path('', views.chat_view, name='home'),
    path('chatroom/<chatroom_name>', views.chat_view, name='chat'),
    path('chat/newgrpchat', views.create_newgrpchat, name='newgrpchat'),
    path('chat/edit_group/<chatroom_name>', views.edit_group, name='edit_group'),
    path('chat/delete_chatroom/<chatroom_name>', views.delete_chatroom, name='delete_chatroom'),
    path('chat/leave_chatroom/<chatroom_name>', views.leave_chatroom, name='leave_chatroom'),
    path('chat/<username>', views.get_or_create_chat, name='start-chat'),
]