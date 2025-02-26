from email.policy import default

from django.conf import settings
from django.db import models
from django.db.models import SET_NULL
from django.core.validators import MaxValueValidator, MinValueValidator

from servers.utils import generate_random_mac_address
from vps_shop import settings


class Vps(models.Model):
    uid = models.AutoField(primary_key=True, verbose_name='Uniq ID')
    name = models.CharField(max_length=60, verbose_name='Name')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, verbose_name='User owner')
    cpu_cores = models.SmallIntegerField(validators=[MaxValueValidator(32), MinValueValidator(1)], default=1, verbose_name='Count cpu cores')
    ram = models.SmallIntegerField(validators=[MaxValueValidator(32), MinValueValidator(1)], default=1, verbose_name='Count ram')
    storage = models.SmallIntegerField(validators=[MaxValueValidator(1024), MinValueValidator(15)], default=15, verbose_name='Count storage in Gb')

    ip_address_private = models.GenericIPAddressField(protocol='IPv4', verbose_name='Private ip', blank=True, null=True)
    ip_address_public = models.GenericIPAddressField(protocol='IPv4', blank=True, unique=True, null=True, verbose_name='Public ip if is')
    mac_address = models.CharField(max_length=48, unique=True, null=True, default=generate_random_mac_address, verbose_name='Mac address')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Time update')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'VPS'
        verbose_name_plural = 'VPS'