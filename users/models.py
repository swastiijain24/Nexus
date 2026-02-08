from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    profileimg = models.ImageField(upload_to='avatars',default='blank-profile-picture.png')
    about = models.TextField(blank=True)

    def __str__(self):
        return self.user_id.username