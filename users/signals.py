from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from allauth.account.models import EmailAddress

# this is a signal that every time a user is created create a profile object for them

@receiver(post_save, sender=User)
def user_postsave(sender, instance, created, **kwargs):
    user = instance

    if created:
        Profile.objects.create(user_id = user)
    else:
        try:
            emailadd = EmailAddress.objects.get_primary(user)
            if emailadd.email != user.email:
                emailadd.email=user.email
                emailadd.verified=False
                emailadd.save()
        except:
            EmailAddress.objects.create(
                user=user, email = user.email, primary=True, verified=False
            )