from django import forms
from django.contrib.auth import (authenticate,get_user_model,login,logout,)

from .models import Post

User=get_user_model()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self ,*args,**kwargs):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")

        # user_qs=User.objects.filter(username=username)
        # if user_qs.count()==1:
        #     user=user_qs.first()
        if username and password:
            user=authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("User doesn't exist.")

            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")

            if not user.is_active:
                raise forms.ValidationError("The user is no longer active.")

        return super(UserLoginForm,self).clean(*args,**kwargs)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password',
        ]
