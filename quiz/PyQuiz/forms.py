from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile, Address
from allauth.account.forms import LoginForm


class CustomCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ( "username","email")
        # app_label = "PyQuiz"
        
        
class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ("username", "email")
        # app_label = "PyQuiz"
        
class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2"]
        # app_label = "PyQuiz"
        
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["name", "email"]
        # app_label = "PyQuiz"
        
class profileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ["address", "image"]
        # app_label = "PyQuiz"

class UserLoginForm(LoginForm):
    email = forms.EmailField(),
    
    class Meta:
        model = User
        feilds = ["email", "password"]
        # app_label = "PyQuiz"
    
# class EmailAddress(LoginForm):
    
#     class Meta:
#         app_label = "PyQuiz"
