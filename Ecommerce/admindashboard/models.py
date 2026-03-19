from django.db import models


class admin_user(models.Model):
    name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)

    def __str__(self):
        return self.name


class product(models.Model):
    pname = models.CharField(max_length=225)
    pprice = models.CharField(max_length=225)
    pdescription = models.TextField()
    pphoto = models.ImageField(upload_to='product_photo/')
    ptype = models.CharField(max_length=225)

    def __str__(self):
        return self.pname
