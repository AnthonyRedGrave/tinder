# Generated by Django 3.1.7 on 2021-03-01 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_app', '0008_delete_profilefortoday'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_dislike', to='tinder_app.profile', verbose_name='От кого')),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_dislike', to='tinder_app.profile', verbose_name='Кому')),
            ],
            options={
                'verbose_name': 'Дизлайк',
                'verbose_name_plural': 'Дизлайки',
            },
        ),
    ]