# Generated by Django 3.1.7 on 2021-03-02 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_app', '0010_chat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reciprocity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rep_user_1', to='tinder_app.profile', verbose_name='От кого')),
                ('user_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rep_user_2', to='tinder_app.profile', verbose_name='Кому')),
            ],
            options={
                'verbose_name': 'Взаимность',
                'verbose_name_plural': 'Взаимности',
            },
        ),
    ]
