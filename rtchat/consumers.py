from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from rtchat.models import *

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(GroupChat, groupname=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        # Only process for authenticated users
        if self.user.is_authenticated:
            if self.user not in self.chatroom.online_users.all():
                self.chatroom.online_users.add(self.user)
                self.update_online_count()

            if self.chatroom.groupchat_name:
                UserChannel.objects.create(member=self.user, group=self.chatroom, channel=self.channel_name)
                self.update_member_count()

        self.accept()

    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

    
        if self.user.is_authenticated:
            if self.user in self.chatroom.online_users.all():
                self.chatroom.online_users.remove(self.user)
                self.update_online_count()

            UserChannel.objects.filter(channel=self.channel_name).delete()
        

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        message = GroupMessage.objects.create(
            body=body,
            group = self.chatroom,
            author = self.user,
        )

        event= {
            'type': 'message_handler',
            'message_id':message.id
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
        }
        html = render_to_string('rtchat/partials/chat_message_p.html', context)
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.online_users.count() -1

        event={
            'type':'online_count_handler',
            'online_count': online_count
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def update_member_count(self):
        # Refresh from database to get current count
        self.chatroom.refresh_from_db()
        member_count = self.chatroom.group_members.count()

        event = {
            'type': 'member_count_handler',
            'member_count': member_count
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def online_count_handler(self, event):
        online_count = event['online_count']
        context={
            'online_count':online_count,
            'chat_group':self.chatroom
        }
        html = render_to_string('rtchat/partials/online_count_p.html', context)
        self.send(text_data=html)

    def user_removed_handler(self, event):
        self.send(text_data=json.dumps({
            'type': 'redirect',
            'url': '/'
        }))

    def member_count_handler(self, event):
        # Refresh chatroom to get latest member data
        self.chatroom.refresh_from_db()
        
        member_count = event['member_count']
        context = {
            'member_count': member_count,
            'chat_group': self.chatroom
        }
        
        # Send member count update
        html = render_to_string('rtchat/partials/member_count_p.html', context)
        self.send(text_data=html)
        
        # Send member list update (avatars)
        members_html = render_to_string('rtchat/partials/groupchat_members_p.html', context)
        self.send(text_data=members_html)
