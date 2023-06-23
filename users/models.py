from django.db import models

from django.contrib.auth.models import AbstractUser, AbstractBaseUser
#from django.contrib.auth.models import User

#signal 
from django.db.models.signals import post_save
from django.dispatch import receiver



class User(AbstractBaseUser):
    #TODO User definition fields
    email = models.EmailField(unique=True, null=True, blank=False)
    username = models.CharField(max_length=25, unique=True)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    
    def __str__(self):
        return f"{self.email}"


class UserProfile(models.Model):
    display_name = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    mfa_security = models.BooleanField(default=True)
    
    # MFA Security
    #TODO List a set of predetermined recovery questions and change recovery_question 
    # field to TextChoice field
    recovery_question = models.CharField(max_length=100)
    recovery_answer = models.CharField(max_length=20)


    def __str__(self) -> str:
        return f"{self.user.username}"




# Signal triggered upon creation of a new user to create a UserProfile for that user 
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()