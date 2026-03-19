from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=225)),
                ('pprice', models.CharField(max_length=225)),
                ('pdescription', models.TextField()),
                ('pphoto', models.ImageField(upload_to='product_photo/')),
                ('ptype', models.CharField(max_length=225)),
            ],
        ),
    ]
