from django.db import models

class user():
    mail = models.CharField(max_length=20)
    first_name = models.TextField()
    last_name = models.TextField()
    password = models.CharField(max_length=20)
    money = models.IntegerField(default=0)
