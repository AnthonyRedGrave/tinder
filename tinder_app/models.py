from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils import timezone


class Profile(models.Model):
    TYPES = (
        ('Man', 'Мужчина'),
        ('Woman', 'Женщина'),
    )

    SUBSCRIPTION_TYPES = (
        ('1', 'Базовая'),
        ('2', 'Вип'),
        ('3', 'Премиум'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField('Никнейм', max_length=150)
    firstname = models.CharField('Имя', max_length=150)
    lastname = models.CharField('Фамилия', max_length=150)
    location = models.CharField('Локация', max_length=150, null=True, blank=True)
    description = models.CharField('Описание', max_length=150, null=True, blank=True)
    type = models.CharField('Пол', choices=TYPES, max_length=10)
    main_photo = models.ImageField('Главное фото', upload_to='mainphoto/', null=True, blank=True)
    sub_type = models.CharField('Тип подписки', choices=SUBSCRIPTION_TYPES, max_length=10, default=1)

    def __str__(self):
        return 'Профиль: {}'.format(self.nickname)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиля пользователей'
        ordering = ['nickname']


class ProfilePhoto(models.Model):
    image = models.ImageField('Фото', upload_to="photoprofiles/")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profilephoto')
    date_pub = models.DateTimeField('Дата публикации', auto_now=True)

    def __str__(self):
        return "Фото профиля: {}".format(self.profile.nickname)

    class Meta:
        verbose_name = 'Фото профиля'
        verbose_name_plural = 'Фото профилей'
        ordering = ['profile']


class Like(models.Model):
    user_from = models.ForeignKey(Profile, verbose_name='От кого', on_delete=models.CASCADE, related_name='from_like')
    user_to = models.ForeignKey(Profile, verbose_name='Кому', on_delete=models.CASCADE, related_name='to_like')

    def __str__(self):
        return '{} - {}'.format(self.user_from, self.user_to)

    class Meta:
        unique_together = ('user_from', 'user_to')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class UnLike(models.Model):
    user_from = models.ForeignKey(Profile, verbose_name='От кого', on_delete=models.CASCADE, related_name='from_dislike')
    user_to = models.ForeignKey(Profile, verbose_name='Кому', on_delete=models.CASCADE, related_name='to_dislike')

    def __str__(self):
        return '{} - {}'.format(self.user_from, self.user_to)

    class Meta:
        unique_together = ('user_from', 'user_to')
        verbose_name = 'Дизлайк'
        verbose_name_plural = 'Дизлайки'


class Reciprocity(models.Model):
    user_1 = models.ForeignKey(Profile, verbose_name='От кого', on_delete=models.CASCADE,
                                  related_name='rep_user_1')
    user_2 = models.ForeignKey(Profile, verbose_name='Кому', on_delete=models.CASCADE, related_name='rep_user_2')

    def __str__(self):
        return 'Взаимность между {} - {}'.format(self.user_1, self.user_2)

    class Meta:
        unique_together = ('user_1', 'user_2')
        verbose_name = 'Взаимность'
        verbose_name_plural = 'Взаимности'


class Chat(models.Model):
    member_1 = models.ForeignKey(Profile, verbose_name='Участник_1', on_delete=models.CASCADE, related_name='member_chat_1')
    member_2 = models.ForeignKey(Profile, verbose_name='Участник_2', on_delete=models.CASCADE, related_name='member_chat_2')
    date = models.DateTimeField(auto_now=True, verbose_name='Начало общения')

    def __str__(self):
        return 'Чат между {} и {}'.format(self.member_1, self.member_2)

    def get_absolute_url(self):
        return reverse('chat', kwargs={'id': self.id})

    class Meta:
        unique_together = ('member_1', 'member_2')
        verbose_name = 'Чат'
        verbose_name_plural = 'Чат'


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE, related_name='message')
    author = models.ForeignKey(Profile, verbose_name='Пользователь', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(verbose_name='Дата сообщения', default=timezone.now)
    is_reader = models.BooleanField('Прочитано', default=False)
    message = models.TextField("Сообщение")

    def __str__(self):
        return '{} {} {}'.format(self.author, self.message, self.pub_date)

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

