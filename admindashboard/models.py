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

class order(models.Model):
    user = models.CharField(max_length=225)
    email = models.EmailField(max_length=225)
    pname = models.CharField(max_length=225, default='Unknown')
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    ptype = models.CharField(max_length=225)
    pprice = models.CharField(max_length=225)
    p_photo = models.ImageField(upload_to='product_photo/')
    pdescription = models.TextField()
    quantity = models.IntegerField()
    total_price = models.CharField(max_length=225)
    order_shipped_status = models.CharField(max_length=225, default='Pending')
