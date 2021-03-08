# Generated by Django 3.1.7 on 2021-03-08 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_app', '0018_auto_20210308_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sub_type',
            field=models.CharField(choices=[('1', 'Базовая'), ('2', 'Вип'), ('3', 'Премиум')], default=1, max_length=10, verbose_name='Тип подписки'),
        ),
    ]
