from .models import Tweet, FormTest, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('title', 'content',)


class ContactForm(forms.Form):
    email = forms.EmailField(required=False)
    title = forms.CharField(required=True)
    text = forms.CharField(widget=forms.Textarea, required=True, min_length=10, max_length=250)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields={
            'bio',
            'gender',
            'image',
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('کاربری با ایمیل وارد شده وجود دارد')
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('کاربری با نام کاربری وارد شده وجود دارد')
        return username

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')
        if password1 != password2:
            raise forms.ValidationError('گذرواژه و تکرار گذرواژه یکسان نیستند')
        return password1

    def save(self, commit=True):
        super(SignUpForm, self).save(commit)


class ImageForm(forms.ModelForm):
    class Meta:
        model = FormTest
        fields = {
            'title',
            'content',
            'image',
        }
