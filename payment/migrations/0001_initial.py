# Generated by Django 4.0.1 on 2022-12-19 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
                ('allowed', models.BooleanField()),
                ('datetime', models.DateTimeField()),
                ('order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detailorders', to='order.order')),
            ],
        ),
    ]
