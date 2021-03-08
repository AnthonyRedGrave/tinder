from rest_framework import serializers
from tinder_app.models import *
from django.contrib.auth.models import User
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class CreateProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user')

    class Meta:
        model = Profile
        fields = ['user_name', 'firstname', 'lastname', 'location', 'description', 'type', 'sub_type', 'main_photo']

    def create(self, validated_data):
        print("profile ser")
        user = User.objects.get(username = validated_data['user_name'])

        if Profile.objects.filter(user = user).exists():# если такой пользователь уже существует
            raise serializers.ValidationError("Такой пользователь уже существует!")

        else:
            print("попал")
            new_profile = Profile.objects.create(user = user,
                                                 nickname = user.username,
                                                 firstname = validated_data['firstname'],
                                                 lastname = validated_data['lastname'],
                                                 location = validated_data['location'],
                                                 description = validated_data['description'],
                                                 type = validated_data['type'],
                                                 sub_type = validated_data['sub_type'],
                                                 main_photo = validated_data['main_photo'])
            return new_profile



# class CreateProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields = ['firstname', 'lastname', 'location', 'description', 'type']


class LikeSerializer(serializers.ModelSerializer):
    u_from = serializers.CharField(source='user_from')
    u_to = serializers.CharField(source='user_to')

    class Meta:
        model = Like
        fields = ['id', 'u_from', 'u_to']

    def create(self, validated_data):
            print("create_ser")
            user_from = Profile.objects.get(nickname = validated_data['u_from'])
            user_to = Profile.objects.get(nickname=validated_data['u_to'])
            if user_from == user_to:
                raise serializers.ValidationError("Пользователи должны быть разными")
            else:
                new_like = Like.objects.create(user_from=user_from, user_to=user_to)
                if Like.objects.filter(user_from = user_to, user_to = user_from).exists(): #если есть взаимный лайк
                    print("есть взаимность")
                    Reciprocity.objects.create(user_1 = user_from, user_2 = user_to)
                    Chat.objects.create(member_1 = user_from, member_2 = user_to)
                    print('чат создан')
                return new_like


class UnLikeSerializer(serializers.ModelSerializer):
    u_from = serializers.CharField(source='user_from')
    u_to = serializers.CharField(source='user_to')

    class Meta:
        model = UnLike
        fields = ['id', 'u_from', 'u_to']


    def create(self, validated_data):
            print("create_ser")
            user_from = Profile.objects.get(nickname = validated_data['u_from'])
            user_to = Profile.objects.get(nickname=validated_data['u_to'])
            if user_from == user_to:
                raise serializers.ValidationError("Пользователи должны быть разными!")

            elif user_from.type == user_to.type:
                raise serializers.ValidationError("Пользователи должны быть противоположны!")

            elif Reciprocity.objects.filter(Q(user_1 = user_from, user_2 = user_to) | Q(user_1 = user_to, user_2 = user_from)).exists(): #если между пользователями взаимность, то лайк поставить нельзя
                raise serializers.ValidationError("Нельзя поставить дизлайк взаимным пользователям!")

            elif Like.objects.filter(Q(user_from = user_from, user_to = user_to) | Q(user_from = user_to, user_to = user_from)).exists(): #если стоит лайк, то дизлайк поставить нельзя
                raise serializers.ValidationError("Нельзя поставить дизлайк!")

            else:
                new_unlike = UnLike.objects.create(user_from=user_from, user_to=user_to)
                return new_unlike


class ReciprocitySerializer(serializers.ModelSerializer):
    u_1 = serializers.CharField(source='user_1')
    u_2 = serializers.CharField(source='user_2')

    class Meta:
        model = Reciprocity
        fields = ['id', 'u_1', 'u_2']


class ChatSerializer(serializers.ModelSerializer):
    m_1 = serializers.CharField(source='member_1')
    m_2 = serializers.CharField(source='member_2')

    class Meta:
        model = Chat
        fields = ['id', 'm_1', 'm_2']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'