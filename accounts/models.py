from django.db import models

from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from accounts.managers import UserManager

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.



class User(AbstractUser):
    username = None # remove username field, we will use email as unique identifier
    email = models.EmailField(unique=True, null=True, db_index=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    
 
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
 
 
    objects = UserManager()

    def __str__(self):
        return f"{self.email}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #display_name = models.CharField(max_length=25, null=True, blank=True)
    phone_number = PhoneNumberField(region='NG', blank=True, null=True)
    phone_number_verified = models.BooleanField(default=False, blank=True, null=True)
    
    # MFA Security
    #TODO List a set of predetermined recovery questions and change recovery_question field to TextChoice field
    mfa_on = models.BooleanField(default=True)
    
    recovery_question = models.CharField(max_length=255)
    recovery_answer = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user.email}"
    
    



class OTPCode(models.Model):
    # TODO Read up on how long it takes to guess/break a four digit code vs a six digit code
    code = models.CharField(max_length=6, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} for {self.owner}"
    
    def send_code(self):
        pass






# Signal triggered upon creation of a new user to create a UserProfile
## for that user 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()