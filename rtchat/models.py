import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class GroupChat(models.Model):
    groupname = models.CharField(max_length=128, unique=True, default=uuid.uuid4)
    groupchat_name = models.CharField(max_length=80, null=True, blank=True)
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='groupchats')
    online_users = models.ManyToManyField(User, related_name='online_users', blank=True)
    group_members= models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)
    recent_msg_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.groupname
    
    class Meta:
        ordering=['-recent_msg_at']
    
class GroupMessage(models.Model):
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500, blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_image(self):
        try:
            self.file.seek(0)
            image = Image.open(self.file)
            image.verify()
            self.file.seek(0)
            return True
        except:
            self.file.seek(0) #Reading a file moves the pointer, seek(0) rewinds it so others can read again.
            return False  
        
    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        else:
            return None

    def __str__(self):
        if self.body:
            return f'{self.author}:{self.body}'
        elif self.file:
            return f'{self.author}:{self.file.url}'
    
    class Meta:
        ordering=['-created_at']

class UserChannel(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, null=True, blank=True)
    channel = models.CharField(max_length=300)