from django.db import models


class Client(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)

    class Meta:
        db_table = 'client'

    def __str__(self):
        return self.name
