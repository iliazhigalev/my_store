import uuid
from datetime import timedelta
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm, UserCreationForm)
from django.utils.timezone import now
from users.models import EmailVerification, User


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль',
    }))

    class Meta:
        model = User
        field = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}))
    gender = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пол'}))
    dob = forms.DateField(widget=MyDateInput({
        'class': 'form-control py-4'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=24)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'dob', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'}), required=False)
    gender = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))
    dob = forms.DateField(widget=MyDateInput({
        'class': 'form-control py-4'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'gender', 'dob', 'username', 'email')
