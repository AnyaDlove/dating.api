from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
    ]
    STATUS_CHOICES = [
        ("search", "В поиске"),
        ("busy", "Занят"),
    ]
    PRIVACY_CHOICES = [
        ("public", "Публичный"),
        ("private", "Приватный"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(18), MaxValueValidator(99)],
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="search")
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default="public")

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"
