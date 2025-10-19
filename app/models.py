from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('dealer', 'Dealer'),
        ('customer', 'Customer'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    state = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.user.username


class Dealer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name_of_company = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
