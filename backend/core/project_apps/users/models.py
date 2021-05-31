from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from project_apps.plans.models import Plan


class CustomUser(AbstractUser):
    plan = models.ForeignKey(Plan,
                             on_delete=models.PROTECT,
                             default=1)

    def get_available_thumbnail_sizes(self):
        user_plan = Plan.objects.filter(pk=self.plan.id).first()
        available_thumbnail_sizes = user_plan.get_available_thumbnail_sizes_list()
        return available_thumbnail_sizes

