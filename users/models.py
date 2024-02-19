from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from materials.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}

PAYMENT_CHOICE = (
    ('cash', 'Наличные'),
    ('transfer', 'Перевод на счет')
)


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER, verbose_name='Роль')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'Пользователь - {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    date_of_payment = models.DateField(auto_now=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', **NULLABLE)
    payment_amount = models.SmallIntegerField(verbose_name='Сумма оплаты', null=True)
    payment_method = models.CharField(max_length=8, default='transfer', choices=PAYMENT_CHOICE,
                                      verbose_name='Способ оплаты', null=True)

    def __str__(self):
        if self.course:
            return f'Курс {self.course.title} оплачен на сумму {self.payment_amount}'
        return f'Урок {self.lesson.title} оплачен на сумму {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
