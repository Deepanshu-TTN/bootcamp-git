from django.db import models

class AppModel(models.Model):
    some_field = models.CharField(max_length=100)