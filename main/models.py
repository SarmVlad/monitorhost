from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    #use_in_migrations = True

    def create_user(self, username, first_name, last_name, email, password=None):
        """
        Creates and saves a User
        """
        if not username:
            raise ValueError('Users must have an username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password):
        """
        Creates and saves a superuser
        """
        user = self.create_user(username, first_name, last_name, email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = MyUserManager()

    username = models.CharField(verbose_name='username', max_length=20, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=25)
    last_name = models.CharField(verbose_name='last name', max_length=25)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    money = models.FloatField(verbose_name='money of user', default=0)
    activation_code = models.CharField(max_length=20, default=objects.make_random_password(length=20))
    password_recovery_code = models.CharField(max_length=20, default='None')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return '%s : %s %s : %s' % (self.username, self.first_name, self.last_name, self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def send_email(self, subject, message):
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)

    def send_hemail(self, subject, html):
        htmly = get_template(html)
        context = { 'user_name' : self.username, 'full_name' : self.get_full_name() , 'activation_code' : self.activation_code}
        html_content = htmly.render(context)
        msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [self.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def password_recovery(self):
        self.password_recovery_code = MyUserManager.make_random_password(self, length=20)
        self.save()
        htmly = get_template('pass_recovery_email.html')
        context = {'username': self.username, 'full_name': self.get_full_name(),
                   'pass_code': self.password_recovery_code}
        html_content = htmly.render(context)
        msg = EmailMultiAlternatives('Запрос на восстановление пароля', '', settings.EMAIL_HOST_USER, [self.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



