from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile


class SignUpForm(UserCreationForm):
    '''
    This form returns the fields needed to create a user
    The email and password fields. The second password field is the password confirmation field.
    '''
    #email = forms.EmailField(max_length=120, help_text="Required. Type in your email")
    #Add additional fields to request for on sign up

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class SetUpMFAForm(forms.ModelForm):
    '''
    This forms returns the three fields on a userprofile needed to setup MFA for this user.
    '''
    class Meta:
        model = UserProfile
        fields =['recovery_question', 'recovery_answer']
