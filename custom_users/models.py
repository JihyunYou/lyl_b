from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

class Users(AbstractUser):
    userType = models.IntegerField(
        default=4,
        validators=[
            MaxValueValidator(4)
        ]
    )

    userFullName = models.CharField(max_length=10)

    userBirthdate = models.DateField
    userSex = models.CharField(max_length=1)

    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    userPhone = models.CharField(validators=[phoneNumberRegex], max_length=11)