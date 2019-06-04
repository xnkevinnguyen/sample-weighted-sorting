from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


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

        print("Creating a super - user for " + kwargs['email'])

        email = self.normalize_email(kwargs['email'])

        user = self.model(**kwargs)

        user.set_password(kwargs['password'])

        # user = self.create_user(**kwargs)

        print("Setting super user properties for " + kwargs['email'])

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class StoreUserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represents a user profile inside our system"""

    email = models.EmailField(max_length=40, unique=True)
    store_name = models.CharField(max_length=30, blank=False, default="")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '5143339994'. between 9-15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False, default="1112223333")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['store_name']

    def get_store_name(self):
        """Used to get a users short name"""
        return self.store_name

    def __str__(self):
        """Print object as a string"""
        return self.email


class StoreItem(models.Model):
    """Represents an item of a Store"""
    store_user = models.ForeignKey(StoreUserProfile, on_delete=models.SET_NULL, null=True ,related_name='store_items')
    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=30, blank=False, default="")
    price=models.IntegerField(null=True)
    created_on =models.DateTimeField(auto_now_add=True, null=True)

    objects = BaseUserManager()

    def ___str___(self):
        """Returns the model as a string"""
        return self.item_name