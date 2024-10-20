from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

    @property
    def has_income(self):
        """if the user has income that is not the default amount"""
        income = self.income_set.all().first()
        return True if income.amount > 0.00 else False
        ...

    def __str__(self):
        return self.email