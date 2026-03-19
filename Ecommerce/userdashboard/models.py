from django.db import models

# Create your models here.

class signup(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    mobile_number = models.BigIntegerField()
    profile_image = models.ImageField(upload_to='profile_images/', )
    address = models.TextField(max_length=255)

    def __str__(self):
        return self.username