from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError('User must have a password')
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # admin
    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,           
        )
        user.admin = True
        user.is_staff = True
        user.first_name = " "
        user.last_name = " "
        user.wallet_address = " "
        user.save(using=self._db)
        return user

    
    def create_player(self, email, password, first_name, last_name, wallet_address):  
        user = self.create_user(
            email,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.wallet_address = wallet_address
        user.player = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=300)
    first_name = models.CharField(max_length=100,default="")
    last_name = models.CharField(max_length=100, default="")
    wallet_address = models.CharField(max_length=100, unique=True)
    admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    player = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        # if self.first_name != None:
        #     return self.first_name
        # else:
        return self.email 

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        return self.admin
    
