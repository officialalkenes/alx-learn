from django.db import models
from django.forms import ValidationError
from django.utils import timezone


from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Manager(BaseUserManager):
    def create_user(self, email, username, fullname, password, **other_fields):
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_staff', False)
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, fullname=fullname, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, fullname, password=None, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_superuser') is not True:
            raise ValidationError("Superuser Field must be set to 'True'. ")
        if other_fields.get('is_staff') is not True:
            raise ValidationError("Superuser must have staff set to 'True'. ")
        return self.create_user(email, username, fullname, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email Address', unique=True,
                              help_text='Only validated Emails are required here')
    username = models.CharField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_verified =models.BooleanField(_('email_verify'),
        default=False,
        help_text=_(
            "Designates whether this user's email has been Verified. "
        ),
    )
    objects = Manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    def __str__(self):
        return f'{self.username}'

    class Meta:
        ordering = ['-date_joined']


GENDER = (
    ('M', 'MALE'),
    ('F', 'FEMALE'),
    ('U', 'UNSPECIFIED')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'), null=True,
                                     blank=True)
    bio = models.TextField(blank=True, null=True,
                                verbose_name= _("About Me"))
    gender = models.CharField(max_length=20, choices=GENDER, default='UNSPECIFIED')
    number = models.PositiveBigIntegerField(_("Telephone Number"), blank=True, null=True)
    ref = models.CharField(max_length=12, verbose_name='Ref', blank=True)
    github = models.URLField(max_length=10, blank=True, null=True, verbose_name ='Github Profile Link')
    linkedIn = models.URLField(max_length=10, blank=True, null=True, verbose_name ='LinkedIn Profile Link')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.gender}'

