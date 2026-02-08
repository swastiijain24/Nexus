import uuid
from django.db import models
from django.contrib.auth.models import User

class GroupChat(models.Model):
    groupname = models.CharField(max_length=128, unique=True, default=uuid.uuid4)
    groupchat_name = models.CharField(max_length=80, null=True, blank=True)
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='groupchats')
    online_users = models.ManyToManyField(User, related_name='online_users', blank=True)
    group_members= models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.groupname
    
class GroupMessage(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}:{self.body}'
    
    class Meta:
        ordering=['-created_at']

class UserChannel(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, null=True, blank=True)
    channel = models.CharField(max_length=300)