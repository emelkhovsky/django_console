from django.db import models

class Ipdata_model(models.Model):
    ip_username = models.CharField(max_length= 50, blank=True)
    ip_ip = models.CharField(max_length=15, blank=True)
    ip_user = models.CharField(max_length=50, blank=True)
    ip_password = models.CharField(max_length=50, blank=True)

    objects = models.Manager()#иначе выдает ошибку, где в views.py пишу objects

    class Meta:
        managed = False
        db_table = 'IP_DB'
