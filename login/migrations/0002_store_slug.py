# Generated by Django 4.0.4 on 2022-12-27 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='slug',
            field=models.CharField(default='store-slug', max_length=50, unique=True),
        ),
    ]
