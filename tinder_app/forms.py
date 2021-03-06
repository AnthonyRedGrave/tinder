from django import forms
from .models import *
from django.contrib.auth.models import User


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Логин"
        self.fields['password'].label = "Пароль"

    def clean(self):

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not User.objects.filter(username = username).exists():
            forms.ValidationError("Пользователь с логином {} не найден".format(username))

        user = User.objects.filter(username = username).first()#первый пользователь с таким логином
        if user:
            if not user.check_password(password):#если пароль не соответствует
                raise forms.ValidationError("Неверный пароль")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterForm(forms.ModelForm):
    TYPES = (
        ('Man', 'Мужчина'),
        ('Woman', 'Женщина'),
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    type = forms.ChoiceField(choices=TYPES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтверждение пароля'
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['firstname'].label = 'Имя'
        self.fields['lastname'].label = 'Фамилия'
        self.fields['type'].label = 'Пол'


    def clean_email(self):
        email = self.cleaned_data['email']
        domain_name = email.split('.')[-1]
        if domain_name in ['com', 'net']:
            raise forms.ValidationError("Регистрация с доменом {} невозможна".format(domain_name))
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Пользователь с таким адресом эл. почты уже существует")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username = username).exists():# если пользователь с таким именем уже существует
            raise forms.ValidationError("Пользователь с таким логином уже существует")
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email', 'firstname', 'lastname', 'type']