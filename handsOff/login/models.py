from django.db import models

# Create your models here.

class Account(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, primary_key=True)
    password = models.CharField(max_length=100)
    phone = models.IntegerField()