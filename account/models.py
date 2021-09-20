# models отвечает за работу с БД
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """данный метод используется для того, чтобы не переписывать два нижеследующих
    метода дважды, избегая дублирования кода"""
    def _create(self, email, password, name, **extra_fields):
        if not email:  # проверяется, есть ли email
            raise ValueError('Email не может быть пустым')
        email = self.normalize_email(email)  # нормализует email, проверка на наличие @ и тд
        user = self.model(email=email, name=name, **extra_fields)
        # создаётся пользователь
        user.set_password(password)
        user.save()  # метод save() сохраняет любые изменения которые произошли в поле
        return user

    # создаёт обычного пользователя
    def create_user(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_staff', False)  # метод setdefault это метод словарей,
        # который устанавливает значение по умолчанию
        extra_fields.setdefault('is_active', False)
        return self._create(email, password, name, **extra_fields)

    # создаёт админов чтобы создать через manage.py создавать superuser
    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, name, **extra_fields)

# Create your models here.
class User(AbstractBaseUser):
    """
    Модель пользователя
    """
    email = models.EmailField('Электронная почта', primary_key=True)
    name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50, blank=True)
    is_active = models.BooleanField('Активный?', default=False)
    is_staff = models.BooleanField('Админ?', default=False)
    activation_code = models.CharField('Код активации', max_length=8, blank=True)

    # привязка менеджера
    objects = UserManager()

    # указывает поле которое будет использоваться в качестве логина
    USERNAME_FIELD = 'email'
    # указываются обязательные поля, кроме username и password, во избежания ошибок при создании
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.email


    """в двух нижеследующих методах определяем какие пользователи
    могут иметь доступ к админ панели"""
    def has_module_perms(self, app_label):  # получаем доступ в админ панели к определенным приложениям
        return self.is_staff


    def has_perm(self, obj=None):
        return self.is_staff

    """метод для создания кода активации"""
    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(8)  # указываем кол-во символов (эту строку можно не писать, а присвоение сделать
        # без переменной
        self.activation_code = code  # присваиваем ему созданный код
        self.save()  # сохраняем

    """создаём свой собственный метод для отправки писем на почту:"""
    def send_activation_mail(self):
        from django.core.mail import send_mail
        message = f'Ваш код активации: {self.activation_code}'
        send_mail('Активация аккаунта',
                  message,
                  'test@test.com',
                  [self.email])
