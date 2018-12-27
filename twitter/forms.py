from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class ContactForm(forms.Form):
    email = forms.EmailField(required=False)
    title = forms.CharField(required=True)
    text = forms.CharField(widget=forms.Textarea, required=True, min_length=10, max_length=250)


class EditProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    bio = forms.CharField(required=False)
    gender = forms.ChoiceField(required=False, choices=(('M', 'Male'), ('F', 'Female')))
    model_pic = forms.ImageField(required=False)
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, )
    CHOICES = [('student', 'student'),
               ('professor', 'professor')]

    type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

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
        id = super(SignUpForm, self).save(commit)
        type = self.cleaned_data['type']
        if type == 'student':
            Group.objects.get(name=type).user_set.add(self.instance)
        elif type == 'professor':
            Group.objects.get(name=type).user_set.add(self.instance)
        else:
            raise forms.ValidationError("چه")
