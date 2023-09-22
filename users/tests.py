from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .forms import UserLoginForm
from .models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Valerii',
            'last_name': 'Pavlikov',
            'gender': 'man',
            'dob': '20.09.2023',
            'username': 'valerii',
            'email': 'valerypavlikov@yandex.ru',
            'password1': '12345678pP',
            'password2': '12345678pP',

        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'zhigalev_store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # self.assertRedirects(response,reverse('users:login'))# надо исправить
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='valerii',
            email='valerypavlikov@yandex.ru',
            password='12345678pP')
        self.login_url = reverse('users:login')

    def test_login_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_success(self):
        data = {
            'username': 'valerii',
            'password': '12345678pP'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, reverse('index'))

    def test_login_error(self):
        data = {
            'username': 'valerii',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertTrue(response.context['form'].errors)
