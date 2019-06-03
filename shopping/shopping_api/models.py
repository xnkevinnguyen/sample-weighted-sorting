from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django.core.validators import URLValidator

from django.db import models


# Create your models here.
class UserProfileManager(BaseUserManager):
    """Our custom user model"""

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


class CandidateProfile(models.Model):
    """ Represents a  candidate profile, extends UserProfile"""
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True, unique=True,
                                        related_name='user_profile_candidate')

    """birth_date (YYYY-MM-DD)"""
    birth_date_regex = RegexValidator(regex=r'^\+?1?\d{8}$',
                                      message="Birthdate must be entered in the format: 'YYYY-MM-DD'")
    birth_date = models.CharField(validators=[birth_date_regex], max_length=8, blank=True, default="20000101")

    """Array of Keys of formation"""
    formation = models.IntegerField(blank=True, default=0)

    """Postal Code XXX YYY"""
    postal_code_regex = RegexValidator(regex='^.{6}$', message='Length has to be 6')
    postal_code = models.CharField(validators=[postal_code_regex], blank=True, max_length=6, default="XXXYYY")

    url_validator = URLValidator(message="This is not a valid url.")
    instagram_url = models.CharField(validators=[url_validator], blank=True, max_length=100)

    """Array of Keys of specialities"""
    specialities = ArrayField(models.IntegerField(), default=[0])

    schedule = models.IntegerField(blank=True, default=0)

    availability_date = models.CharField(max_length=30, blank=True, default="Now", null=True)

    objects = UserProfileManager()


class EmployerProfile(models.Model):
    """Represents an enterprise user, extends UserProfile"""
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True, unique=True,
                                        related_name='user_profile_employer')
    employer_name = models.CharField(max_length=30, blank=False, default="")

    address = models.CharField(max_length=60, blank=False, default="")

    office_number = models.IntegerField(blank=True, default=0)

    commercial_category = models.IntegerField(blank=False, default=0)

    specialty_demand = ArrayField(models.IntegerField(), default=[0])

    hiring_number = models.IntegerField(blank=True, default=0)

    url_validator = URLValidator(message="This is not a valid url.")
    website_url = models.CharField(validators=[url_validator], blank=True, max_length=100)

    objects = UserProfileManager()
