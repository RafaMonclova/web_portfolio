from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

from django.utils.translation import gettext_lazy as _
from enum import Enum

class User(AbstractUser):
    pass
