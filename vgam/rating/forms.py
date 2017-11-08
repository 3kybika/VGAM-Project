# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rating.models import *


class RegistrationForm(forms.Form):
    title = 'Регистрация нового пользователя'
    username = forms.CharField(
        widget = forms.TextInput(attrs = {
            'class': 'form-control input-sm',
            'placeholder': 'Login',
            'title': 'Логин:',
        })
    )
    username.label = 'Логин:'
    
    email = forms.EmailField(
        widget = forms.EmailInput(attrs = {
            'class': 'form-control input-sm',
            'placeholder': 'E-mail',
            'title': 'Электронная почта:',
        })
    )
    email.label = 'Электронная почта:'

    password = forms.CharField(
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control input-sm',
            'placeholder': 'Password',
            'title': 'Введите пароль:',
        })
    )
    password.label = 'Введите пароль:'

    confirm_password = forms.CharField(
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control input-sm',
            'placeholder': 'Repeat password',
            'title': 'Подтвердите пароль:',
        })
    )
    confirm_password.label = 'Подтвердите пароль:'

    avatar = forms.ImageField(
        required = False, widget = forms.FileInput(attrs = {
            'class': 'form-control input-lg',
            'title': 'Аватар:',
        })
    )
    avatar.label = 'Аватар:'
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username = username):
            raise forms.ValidationError('Пользователь с таким именем уже существует!')
        return username

    def clean_confirm_password(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError('Введенные Вами пароли не совпадают!')
        return data['confirm_password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email):
            raise forms.ValidationError('Пользователь с такитм e-mail-ом уже зарегистрирован!')
        return email

    def save(self):
        data = self.cleaned_data
        username = data['username']
        email = data['email']
        password = data['password']
        new_user = User.objects.create_user(username = username, email = email, password = password)
        if self.cleaned_data['avatar'] is not None:
            profile = Profile(User = new_user, avatar = self.cleaned_data['avatar'])
            profile.save()
        else:
            profile = Profile(User = new_user)
            profile.save()


class LoginForm(forms.Form):
    title = 'Авторизация:'
    username = forms.CharField(
        widget = forms.TextInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Login',
        })
    )
    username.label = 'Логин:'

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
            'class' : 'form-control',
            'placeholder' : 'Password',
        })
    )
    password.label = 'Пароль:'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        self.user = authenticate(username = username, password = password)

        if self.user is None:
            raise forms.ValidationError('Неверный логин или пароль!')