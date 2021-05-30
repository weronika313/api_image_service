from django.contrib.auth.models import AbstractUser
from django.db import models
from project_apps.plans.models import Plan

class CustomUser(AbstractUser):
    plan = models.ForeignKey(Plan,
                             on_delete=models.PROTECT,
                             default=1)
