from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator



# Create your models here.

class UserProfileManager(BaseUserManager):
    """Custom Client Model"""

    def create_user(self, **kwargs):
        """ Constructor for our profile object"""

        if not kwargs["email"]:
            raise ValueError('Users must have an email address.')

        print("Creating a user for " + kwargs['first_name'])

        email = self.normalize_email(kwargs['email'])

        user = self.model(**kwargs)

        user.set_password(kwargs['password'])

        user.save(using=self._db)

        return user

    def create_superuser(self, **kwargs):
        """Constructor for a superuser"""

        print("Creating a super - user for " + kwargs['first_name'])

        email = self.normalize_email(kwargs['email'])

        user = self.model(**kwargs)

        user.set_password(kwargs['password'])

        # user = self.create_user(**kwargs)

        print("Setting super user properties for " + kwargs['first_name'])

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represents a user profile inside our system"""

    is_candidate = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=False, default="")
    last_name = models.CharField(max_length=30, blank=False, default="")
    last_name2 = models.CharField(max_length=30, blank=False, default="")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '5143339994'. between 9-15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False, default="1112223333")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_first_name(self):
        """ Used to get a users name."""

        return self.first_name

    def get_last_name(self):
        """Used to get a users short name"""
        return self.last_name

    def __str__(self):
        """Print object as a string"""

        return self.email