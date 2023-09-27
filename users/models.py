from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    dob = models.DateField(max_length=8, null=True, blank=True)  # Дата рождения
    gender = models.CharField(max_length=15)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    is_verirified_email = models.BooleanField(default=False)  # подтвердил ли пользователь почту

    def __str__(self):
        return f'Пользователь: {self.username} | Электронная почта: {self.email}'

    class Meta:
        verbose_name_plural = 'Пользователи'  # название в админ панели


class EmailVerification(models.Model):
    class Meta:
        verbose_name_plural = 'Хранение почты'  # название в админ панели

    code = models.UUIDField(unique=True, editable=False)  #
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()  # срок действия данной ссылки

    def __str__(self):
        return f'EmailVerification объект для пользователя : {self.user.username} '

    def send_verification(self):
        link = reverse('users:email_verif', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учётной записи для {self.user.username}'
        massagee = 'Для подтверждения учётной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=massagee,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration
