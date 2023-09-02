from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.auth.models import Group

def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_professor(user):
    return user.groups.filter(name='Professor').exists()

class KorisnikManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        username = email.split('@')[0]
        first_name = extra_fields.pop('first_name', '')  # Retrieve the first_name field if provided
        last_name = extra_fields.pop('last_name', '')  # Retrieve the last_name field if provided

        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Korisnik(AbstractUser):
    # Set the 'email' field as the unique identifier for authentication
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Add any additional fields you need (e.g., first name, last name)
    email = models.EmailField(unique=True)  # Add unique=True here
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True)  # Add this line

    objects = KorisnikManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        return super().save(*args, **kwargs)

class Admin(models.Model):
    user = models.OneToOneField(Korisnik, on_delete=models.CASCADE)

    @staticmethod
    def create_admin(user):
        if user.is_superuser:
            admin = Admin.objects.create(user=user)
            return admin

    def create_admin_user(self, email, password, first_name, last_name):
        admin_user = Korisnik.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        admin = Admin.create_admin(admin_user)
        return admin

   


class Profesor(models.Model):
    user = models.OneToOneField(Korisnik, on_delete=models.CASCADE)
    

    @staticmethod
    def create_profesor(user):
        profesor = Profesor.objects.create(user=user)
        return profesor
def create_profesor(self, email, password, first_name, last_name):
        profesor_user = Korisnik.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        profesor = Profesor.create_profesor(profesor_user)
        return profesor
def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Kolegij(models.Model):
    kolegij_id = models.AutoField(primary_key=True)
    kolegij_naziv = models.CharField(max_length=255, default='Default Name')
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.kolegij_naziv

    class Meta:
        verbose_name_plural = "Kolegiji"


    
class Obavijest(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=2000)
    publication_date = models.DateField()
    expiration_date = models.DateField()
    kolegij = models.ForeignKey(Kolegij, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = "Obavijesti"

