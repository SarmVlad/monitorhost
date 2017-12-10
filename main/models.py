from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


#Extension User class
class Panel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activate_link = models.TextField(default=datetime.now)
    reg_date = models.DateTimeField()
    money = models.IntegerField(default=0)
