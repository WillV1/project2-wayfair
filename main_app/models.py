from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

# Create your models here.
class Profile(models.Model):
    current_city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='images')
    join_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.current_city
